import numpy as np
import math
import csv
import socket
import cv2
from sakamoto.camera import camera_measurement
from sakamoto import order_linecar
from sakamoto import order_left
from sakamoto import order_right
import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl

def main():
    cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
    #FPS,解像度の設定
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    sock_left = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock_right = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # IPアドレスとポートを指定
    sock_left.bind(('127.0.0.1', 50006))
    sock_right.bind(('127.0.0.1', 50007))
    #sock_left.bind(('192.168.43.198', 50006))
    #sock_right.bind(('192.168.43.198', 50007))

    # 接続(最大2)
    sock_left.listen(2)
    sock_right.listen(2)
    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
    conn_left, addr_left = sock_left.accept()
    conn_right, addr_right = sock_right.accept()
    record = []
    type_area = "="
    position_record = [sets.POSITION_START[0], sets.POSITION_START[1], sets.POSITION_END[0], sets.POSITION_END[1]]
    camera_record = []
    count = 0
    m1 = LineCar()
    m1.setup4experiment()
    m1.controller.prepare()
    # 発進
    m1.mv_wheel(sets.SPEED)


    while(cap.isOpened()):
        if conn_left or conn_right == "":
            pass
        else:
            if count == 0:
                # データを受け取る
                data_left = conn_left.recv(1024)
                data_right = conn_left.recv(1024)
                print(b'Received: ' + data_left)
                print(b'Received: ' + data_right)
                conn_left.sendall(b'start!!')
                conn_right.sendall(b'start!!')
                count +=1
                data_left = 0
                data_right = 0
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  

        while(True):
            try:  
                now_latlon = m1.get_current_position()
                ret, frame = cap.read()
                distance_left, distance_right, tar_x1, tar_x2, difference_left, difference_right = camera_measurement(ret, frame)
                if now_latlon[3] == 1:
                    angle = m1.controller.get_input_angle(now_latlon)
                    order_left = order_left.order_fix(distance_left, tar_x1)
                    order_right = order_right.order_fix(distance_right, tar_x2)
                
                if now_latlon[3] == 2:
                    angle, type_area = order_linecar.order_float(tar_x1, tar_x2, difference_left, difference_right)
                    order_left = order_left.order_float(distance_left, tar_x1)
                    order_right = order_right.order_float(distance_right, tar_x2)

                m1.mv_angle(angle)
                conn_left.sendall(b(order_left))
                conn_right.sendall(b(order_right))

                record.append(m1.get_status())
                camera_record.append(tar_x1,tar_x2,angle,type_area)
                record = record + camera_record

                if m1.controller.is_finished():
                    m1.mv_wheel(0)
                    conn_left.sendall(b'Stop')
                    conn_right.sendall(b'Stop')
                    break

            except KeyboardInterrupt:
                with open('./output.csv', 'w') as csv_out:
                    writer = csv.writer(csv_out, lineterminator='\n')
                    writer.writerows([position_record])
                    writer.writerows(record)
                m1.stop()

    # 終了処理
    m1.stop()
    cap.release()
    cv2.destroyAllWindows()     

    with open('./output.csv', 'w') as csv_out:
        writer = csv.writer(csv_out, lineterminator='\n')
        writer.writerows([position_record])
        writer.writerows(record)


if __name__ == '__main__':
    main()
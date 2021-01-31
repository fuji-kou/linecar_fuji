import numpy as np
import math
import csv
import socket
import cv2
from camera_settings import camera
from time import sleep
import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl

#カメラキャプチャ
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

TMP_FOLDER_PATH = ".cali/tmp/"
MTX_PATH = TMP_FOLDER_PATH + "mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "dist2.csv"

#FPS,解像度の設定
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def camera_measurement():
    ret, frame = cap.read()
    #キャリブレーション適用
    mtx, dist = camera.loadCalibrationFile(MTX_PATH, DIST_PATH)
    resultImg = cv2.undistort(frame, mtx, dist, None)
    #赤色検出
    mask = camera.red_detect(resultImg)
    w, h = mask.shape
        
    empty_image = np.zeros((w,h), dtype = np.uint8)
    dif = mask - empty_image
    if dif.any() == 0:      #零行列の場合
        pass

    else:
        #マスク画像をブロブ解析（面積最大のブロブ情報を取得）
        target = camera.analysis_blob(mask)
            
        #面積最大ブロブの中心座標を取得
        tar_x1 = int(target["center1"][0])
        tar_y1 = int(target["center1"][1])
            
        tar_x2 = int(target["center2"][0])
        tar_y2 = int(target["center2"][1])
        cv2.line(resultImg,(400,0),(400,720),(0,255,0),3)
        cv2.line(resultImg,(640,0),(640,720),(0,200,0),3)
        cv2.line(resultImg,(880,0),(880,720),(0,200,0),3)   

        #フレームに面積最大ブロブの中心周囲を円で描く
        cv2.circle(resultImg, (tar_x1, tar_y1), 30, (0, 255, 0),
                thickness=3, lineType=cv2.LINE_AA)
            
        if tar_x2 == 0:
            pass
            
        else:
            cv2.circle(resultImg, (tar_x2, tar_y2), 30, (255, 0, 0),
                    thickness=3, lineType=cv2.LINE_AA)  


        #２つの計測対象の面積をリストに格納
        (area1, area2) = (target['area1'], target['area2'])       #赤の面積
        (area1, area2) = (area1/(1280*720)*100, area2/(1280*720)*100)       #割合
        #距離計算の選択
        (area1, area2) = (round(159.55*area1**(-0.525)), round(159.55*area2**(-0.525))) #10-780
        # (area1, area2) = (round(161.24*area1**(-0.553)), round(161.24*area2**(-0.553))) #10-480  
        # (area1, area2) = (round(162.89*area1**(-0.51)), round(162.89*area2**(-0.51))) #400-780
        distance_left = area1
        distance_right = area2
        # 中心座標
        center_x = 640
        center_y = 360
        #中心からのx座標の差
        difference_left = center_x - tar_x1
        difference_right = tar_x2 - center_x
        # print(difference_left , difference_right)

    #表示
    cv2.imshow('Frame', resultImg)
    return distance_left, distance_right, tar_x1, tar_x2, difference_left, difference_right


def main():
    record = []
    count = 0
    fix_or_float = 1
    # ソケット作成
    sock_left = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock_right = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # IPアドレスとポートを指定
    #ファーウェイタブ（ラズパイとの通信）
    #sock.bind(('192.168.43.198', 50007))
    #ファーウェイタブ（ラズパイとの通信)DELL
    sock_left.bind(('192.168.43.198', 50006))
    sock_right.bind(('192.168.43.198', 50007))    
    #linecar用モバイルルータ
    #sock_left.connect(('192.168.179.2', 50008))
    #sock_right.connect(('192.168.179.2', 50009))
    #sock_left.bind(('0.0.0.0', 50008))
    #sock_right.bind(('0.0.0.0', 50009))
    # 接続(最大2)
    sock_left.listen(2)
    sock_right.listen(2)
    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
    conn_left, addr_left = sock_left.accept()
    conn_right, addr_right = sock_right.accept()

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


        #保存
        #writer.write(resultImg)

        #qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  

        # 操作ループ
        while(True):
            try:  
                m1.mv_wheel(sets.SPEED)
                now_latlon = m1.get_current_position()
                distance_left, distance_right, tar_x1, tar_x2, difference_left, difference_right = camera_measurement()
                if now_latlon[3] == 2:
                    m1.mv_wheel(0)
                    m1.mv_angle(0)
                    if fix_or_float == 1:
                        conn_left.sendall(b'Stop1')
                        conn_right.sendall(b'Stop2')
                        fix_or_float = 2
                    print(distance_left,distance_right)

                    if distance_left >= 100 and 400 <= tar_x1 <= 640:
                        conn_left.sendall(b'Go1')
                    if distance_right >= 100 and 640 <= tar_x2 <= 880:
                        conn_right.sendall(b'Go2')

                    if distance_left < 100:
                        conn_left.sendall(b'Stop1')
                    if distance_right < 100:
                        conn_right.sendall(b'Stop2')

                    if distance_left >= 100 and tar_x1 < 400:
                        conn_left.sendall(b'turn_left1')
                    if distance_right >= 100 and tar_x2 < 640:
                        conn_right.sendall(b'turn_left2')

                    if distance_left >= 100 and tar_x1 > 640:
                        conn_left.sendall(b'turn_right1')
                    if distance_right >= 100 and tar_x2 > 880:
                        conn_right.sendall(b'turn_right2')
                    
                    # if difference_left > difference_right:
                    #     angle = math.atan(distance_left/((difference_left - difference_right)/2))
                    #     m1.mv_angle(angle)
                    # if difference_left == difference_right:
                    #     m1.mv_angle(0)
                    # if difference_left < difference_right:
                    #     angle = math.atan(distance_right/((difference_right - difference_left)/2))
                    #     m1.mv_angle(-angle)

                else:
                    if fix_or_float == 2:
                        fix_or_float = 1
                    input_angle = m1.controller.get_input_angle(now_latlon)
                    m1.mv_angle(round(input_angle, 1))


                record.append(m1.get_status())

                if m1.controller.is_finished():
                    m1.mv_wheel(0)
                    break
            except KeyboardInterrupt:
                m1.stop()

    # 終了処理
    m1.stop()
    cap.release()
    cv2.destroyAllWindows()     

    with open('./output.csv', 'w') as csv_out:
        writer = csv.writer(csv_out, lineterminator='\n')
        writer.writerows(record)


if __name__ == '__main__':
    main()

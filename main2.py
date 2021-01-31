import numpy as np
import math
import csv
import socket
import cv2
import time
from camera_settings import camera

import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl

#カメラキャプチャ
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
MTX_PATH = TMP_FOLDER_PATH + "\\mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "\\dist2.csv"

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
    #cv2.imshow('Frame', resultImg)
    return distance_left, distance_right, tar_x1, tar_x2, difference_left, difference_right

def linecar_control_fix():
    pass

def linecar_control_float():
    pass

def left_control_fix():
    pass

def left_control_float():
    pass

def right_control_fix():
    pass

def right_control_float():
    pass



def main():
    record = []
    position_record = [sets.POSITION_START[0], sets.POSITION_START[1], sets.POSITION_END[0], sets.POSITION_END[1]]
    camera_record = []
    count = 0
    fix_or_float = 1
    # ソケット作成
    sock_left = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock_right = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # IPアドレスとポートを指定
    sock_left.bind(('192.168.43.198', 50006))
    sock_right.bind(('192.168.43.198', 50007))

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
                data_left = 0
                data_right = 0

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
                if now_latlon[3] == 1:
                    if fix_or_float == 2:
                        fix_or_float = 1
                        
                    
                    else:
                        if distance_left == None or distance_right == None:
                            conn_left.sendall(b'Stop')
                            conn_right.sendall(b'Stop')
                        else:
                            if distance_left >= 120 and tar_x1 == 375:
                                conn_left.sendall(b'Go')
                            if distance_right >= 120 and tar_x2 == 905:
                                conn_right.sendall(b'Go')

                            if distance_left < 120:
                                conn_left.sendall(b'Stop')
                            if distance_right < 120:
                                conn_right.sendall(b'Stop')

                            # left
                            if distance_left >= 120 and tar_x1 < 250:
                                conn_left.sendall(b'turn_left1')
                            if distance_left >= 120 and 250 <= tar_x1 <= 375:
                                conn_left.sendall(b'turn_left2')

                            if distance_left >= 120 and tar_x1 > 500:
                                conn_left.sendall(b'turn_right1')
                            if distance_left >= 120 and 375 < tar_x1 <= 500:
                                conn_left.sendall(b'turn_right2')
                            
                            # right
                            if distance_right >= 120 and tar_x2 < 780:
                                conn_right.sendall(b'turn_left1')
                            if distance_right >= 120 and 780 < tar_x2 < 905:
                                conn_right.sendall(b'turn_left2')
                                        
                            if distance_right >= 120 and tar_x2 > 1030:
                                conn_right.sendall(b'turn_right1')
                            if distance_right >= 120 and 905 <= tar_x2 < 1030:
                                conn_right.sendall(b'turn_right2')
                    input_angle = m1.controller.get_input_angle(now_latlon)
                    m1.mv_angle(round(input_angle, 1))

                if now_latlon[3] == 2:
                    m1.mv_wheel(0)
                    time.sleep(2)
                    m1.mv_wheel(sets.SPEED)
                    
                    if fix_or_float == 1:
                        conn_left.sendall(b'Stop')
                        conn_right.sendall(b'Stop')
                        fix_or_float = 2
                    #print(distance_left,distance_right)
                    else:
                        if difference_left == None or difference_right == None:
                            m1.mv_wheel(0)
                            m1.mv_angle(0)
                        else:
                            if distance_left >= 120 and tar_x1 == 375:
                                conn_left.sendall(b'Go')
                            if distance_right >= 120 and tar_x2 == 905:
                                conn_right.sendall(b'Go')

                            if distance_left < 400:
                                conn_left.sendall(b'Stop')
                            if distance_right < 400:
                                conn_right.sendall(b'Stop')

                            # left
                            if distance_left >= 400 and tar_x1 < 250:
                                conn_left.sendall(b'turn_left1')
                            if distance_left >= 400 and 250 <= tar_x1 <= 375:
                                conn_left.sendall(b'turn_left2')

                            if distance_left >= 400 and tar_x1 > 500:
                                conn_left.sendall(b'turn_right1')
                            if distance_left >= 400 and 375 < tar_x1 <= 500:
                                conn_left.sendall(b'turn_right2')
                                    
                            # right
                            if distance_right >= 400 and tar_x2 < 780:
                                conn_right.sendall(b'turn_left1')
                            if distance_right >= 400 and 780 < tar_x2 < 905:
                                conn_right.sendall(b'turn_left2')
                                                
                            if distance_right >= 400 and tar_x2 > 1030:
                                conn_right.sendall(b'turn_right1')
                            if distance_right >= 400 and 905 <= tar_x2 < 1030:
                                conn_right.sendall(b'turn_right2')

                        
                            if tar_x1 <= 640 and tar_x2 <= 640:
                                ang
                                le = (tar_x2 - tar_x1)/2 -640
                                angle = angle*6400/(2*math.pi)
                                angle = angle*0.0001
                                type_area = "left_side"
                                print(angle,"left_side")
                            elif tar_x1 > 640 and tar_x2 > 640:
                                angle = 640 - (tar_x2 - tar_x1)/2
                                angle = angle*6400/(2*math.pi)
                                angle = angle*0.0001
                                type_area = "right_side"
                                print(angle,"right_side")
                            else:
                                if difference_left > difference_right:
                                    angle = math.atan(distance_left/((difference_left - difference_right)/2))

                                    angle = angle*6400/(2*math.pi)
                                    angle = angle*0.1
                                    angle = -1*angle
                                    type_area = "left"
                                    print(angle,"left")
                                if difference_left == difference_right:
                                    angle = 0
                                    type_area = "="
                                    print(angle,"=")
                                if difference_left < difference_right:
                                    angle = math.atan(distance_right/((difference_right - difference_left)/2))

                                    angle = angle*6400/(2*math.pi)
                                    angle = angle*0.1
                                    type_area = "right"
                                    print(angle,"right")
                        m1.mv_angle(angle)

                
                    

                record.append(m1.get_status())
                camera_record.append(tar_x1,tar_x2,angle,type_area)
                record = record + camera_record

                if m1.controller.is_finished():
                    m1.mv_wheel(0)
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
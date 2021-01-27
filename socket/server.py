import socket
import numpy as np
import csv

import linecar_settings as sets
import math
import cv2
from camera_settings import camera

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

        cv2.line(resultImg,(150,0),(150,720),(255,0,0),3)
        cv2.line(resultImg,(250,0),(250,720),(255,0,0),3)
        cv2.line(resultImg,(500,0),(500,720),(255,0,0),3)

        cv2.line(resultImg,(640,0),(640,720),(0,255,0),3)

        cv2.line(resultImg,(780,0),(780,720),(0,0,255),3)
        cv2.line(resultImg,(1030,0),(1030,720),(0,0,255),3)
        cv2.line(resultImg,(1130,0),(1130,720),(0,0,255),3)

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
        #real_distance_list1.append(area1)
        #real_distance_list2.append(area2)
    #表示
    cv2.imshow('Frame', resultImg)
    #cv2.imshow("Mask", mask)
    return distance_left , distance_right , tar_x1 , tar_x2

def main():    
    # データ格納用のリスト
    real_distance_list1 = []
    real_distance_list2 = []
    

    count = 0
    # ソケット作成
    sock_left = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock_right = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # IPアドレスとポートを指定
    #同端末DELL
    #sock_left.bind(('127.0.0.1', 50006))
    #sock_right.bind(('127.0.0.1', 50007))
    #宮本研DELL
    # sock_left.bind(('192.168.11.12', 50006))
    # sock_right.bind(('192.168.11.12', 50007))

    #ファーウェイタブ（ラズパイとの通信)DELL
    sock_left.bind(('192.168.43.198', 50006))
    sock_right.bind(('192.168.43.198', 50007))

    #iphone
    #sock_left.bind(('172.20.10.7', 50006))
    #sock_right.bind(('172.20.10.7', 50007))
    #sock_left.connect(('0.0.0.0', 50006))
    #sock_right.connect(('0.0.0.0', 50007))
    
    #実機HP_PC
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
            #print(1)
            #data = 10
            #ループ抜けだし
#            if data == 10:
#                break
        distance_left,distance_lright,tar_x1,tar_x2 = camera_measurement()
        print(distance_left,distance_lright)
        #print(tar_x1,tar_x2)
        if distance_left >= 300 and 250 <= tar_x1 <= 500:
            conn_left.sendall(b'Go1')
        if distance_lright >= 300 and 780 <= tar_x2 <= 1030:
            conn_right.sendall(b'Go2')

        if distance_left < 300:
            conn_left.sendall(b'Stop1')
        if distance_lright < 300:
            conn_right.sendall(b'Stop2')

        if distance_left >= 300 and tar_x1 < 250:
            conn_left.sendall(b'turn_left1')
        if distance_lright >= 300 and tar_x2 < 780:
            conn_right.sendall(b'turn_left2')

        if distance_left >= 300 and tar_x1 > 500:
            conn_left.sendall(b'turn_right1')
        if distance_lright >= 300 and tar_x2 > 1030:
            conn_right.sendall(b'turn_right2')

        # if distance_left >= 300 and tar_x1 > 600:
        #     conn_left.sendall(b'turn_right!1')
        # if distance_lright >= 300 and tar_x2 > 880:
        #     conn_right.sendall(b'turn_right!2')

        # if distance_left >= 300 and tar_x1 > 600:
        #     conn_left.sendall(b'turn_right!!1')
        # if distance_lright >= 300 and tar_x2 > 880:
        #     conn_right.sendall(b'turn_right2!!')


        # #中心座標
        # center_x = 640
        # center_y = 360

        # #中心ピクセルから認識した赤色の中心までを直線描画，cv2.line(画像,座標1,座標2,色,太さ)
        # cv2.line(resultImg,(tar_x1, tar_y1),(640,360),(0,255,0),3)
        # cv2.line(resultImg,(tar_x2, tar_y2),(640,360),(0,200,0),3)

        # #x座標とy座標をピクセルからcmに変換
        # dif_x1 = round(abs(center_x - tar_x1) * (398/1280))
        # dif_y1 = round(abs(center_y - tar_y1) * (107/360))

        # dif_x2 = round(abs(center_x - tar_x2) * (398/1280))
        # dif_y2 = round(abs(center_y - tar_y2) * (107/360))            

        # distance_left = math.sqrt(dif_x1^2 + dif_y1^2)
        # distance_lright = math.sqrt(dif_x2^2 + dif_y2^2)
        # print(distance_left)
        # print(distance_lright)

        #結果表示
        #cv2.imshow('Frame', resultImg)
        #cv2.imshow("Mask", mask)

        #保存
        #writer.write(resultImg)

        #qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    #保存
    cap.release()
    cv2.destroyAllWindows()
    #writer.release()

if __name__ == '__main__':
    main()





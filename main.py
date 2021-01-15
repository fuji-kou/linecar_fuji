import numpy as np
import csv
import socket
import cv2
from camera.camera_settings import camera

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

print(cv2.CAP_PROP_FRAME_WIDTH)

def main():
    record = []
    real_distance_list1 = []
    real_distance_list2 = []

    count = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #ソケット作成
    # IPアドレスとポートを指定
    #ファーウェイタブ（ラズパイとの通信）
    #sock.bind(('192.168.43.198', 50007))
    #linecar用モバイルルータ
    sock.bind(('192.168.179.2', 50007))    

    # 接続(最大2)
    sock.listen(2)
    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
    conn, addr = sock.accept()

    m1 = LineCar()
    m1.setup4experiment()
    m1.controller.prepare()
    # 発進
    m1.mv_wheel(sets.SPEED)


    while(cap.isOpened()):
        if conn == "":
            pass
        else:
            if count == 0:
                # データを受け取る
                data = conn.recv(1024)
                print(b'Received: ' + data)
                conn.sendall(b'start!!!!')
                count +=1
                data = 0
            #print(1)

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
                cv2.circle(resultImg, (tar_x2, tar_y2), 30, (0, 255, 0),
                        thickness=3, lineType=cv2.LINE_AA)  

            #面積最大ブロブの中心座標を取得
            if tar_x1 <= 640:
                (area1, area2) = (target['area1'], target['area2'])       #赤の面積
            if tar_x1 > 640:
                (area1, area2) = (target['area2'], target['area1'])       #赤の面積
            else:
                area1 = target['area1']

            #２つの計測対象の面積をリストに格納
            #(area1, area2) = (target['area1'], target['area2'])       #赤の面積
            (area1, area2) = (area1/(1280*720)*100, area2/(1280*720)*100)       #割合
            (area1, area2) = (round(159.55*area1**(-0.525)), round(159.55*area2**(-0.525))) #10-780
            # (area1, area2) = (round(161.24*area1**(-0.553)), round(161.24*area2**(-0.553))) #10-480  
            # (area1, area2) = (round(162.89*area1**(-0.51)), round(162.89*area2**(-0.51))) #400-780
            real_distance_list1.append(area1)
            real_distance_list2.append(area2)


            if area1 >= 100:
                conn.sendall(b'Go!!!!')
            if area1 < 100:
                conn.sendall(b'Stop!!!!')

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

            # distance1 = math.sqrt(dif_x1^2 + dif_y1^2)
            # distance2 = math.sqrt(dif_x2^2 + dif_y2^2)
            # print(distance1)
            # print(distance2)

        #結果表示
        cv2.imshow('Frame', resultImg)
        #cv2.imshow("Mask", mask)

        #保存
        #writer.write(resultImg)

        #qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  

        # 操作ループ
        while(True):
            try:  
                now_latlon = m1.get_current_position()
                if now_latlon[3] == 2:
                    m1.mv_wheel(0)
                    conn.sendall(b'f_stop')                
                input_angle = m1.controller.get_input_angle(now_latlon)
                m1.mv_angle(round(input_angle, 1))
                record.append(m1.get_status())
                #floutのとき



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

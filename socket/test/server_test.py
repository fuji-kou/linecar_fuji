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



def main():    
    # データ格納用のリスト
    count = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #ソケット作成
    # IPアドレスとポートを指定
    #同端末
    sock.bind(('127.0.0.1', 50007))
    #ファーウェイタブ（ラズパイとの通信）
    #sock.bind(('192.168.43.198', 50007))
    #恐らく宮本研wi-hi（ラズパイとの通信）
    #sock.bind(('255.255.255.0', 50007))

    # 接続(最大2)
    sock.listen(2)
    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
    conn, addr = sock.accept()

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
            print(1)
            data = 10
            #ループ抜けだし
#            if data == 10:
#                break
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




        #             print('data : {}, addr: {}'.format(data, addr))
        #                 # クライアントにデータを返す(b -> byte でないといけない)
        #                 #conn.sendall(b'Received: ' + data)
        #                 #conn.sendall(b'start!!!!')


        #             if data == (b'connect'):
        #                 print(data)
        #                 conn.sendall(b'start!!!!')




    #保存
    cap.release()
    cv2.destroyAllWindows()
    #writer.release()

if __name__ == '__main__':
    main()





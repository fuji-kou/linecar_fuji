import numpy as np
import math
import cv2
import glob
#from time import sleep
import time
import datetime as dt
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


# # #保存
# fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# fps = 10.0
# size = (1280, 720)
# SAVE_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\video\\"
# now = dt.datetime.now()
# time = now.strftime('%Y_%m%d_%H%M_%S')
# writer = cv2.VideoWriter(SAVE_PATH + 'video_{}.mp4'.format(time), fmt, fps, size)



def main():    
    # データ格納用のリスト
    data = []

    # 記録データの保存先パス
    #csvfile_path = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\tracking"
    # 開始時間
    #start = time.time()

    while(cap.isOpened()):
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
            tar_x = int(target["center"][0])
            tar_y = int(target["center"][1])
        
            # フレームに面積最大ブロブの中心周囲を円で描く
            cv2.circle(resultImg, (tar_x, tar_y), 30, (0, 200, 0),
                    thickness=3, lineType=cv2.LINE_AA)

            #中心座標
            center_x = 640
            center_y = 360

            #中心ピクセルから認識した赤色の中心までを直線描画，cv2.line(画像,座標1,座標2,色,太さ)
            cv2.line(resultImg,(tar_x, tar_y),(640,360),(0,255,0),3)

            #x座標とy座標をピクセルからcmに変換
            dif_x = round(abs(center_x - tar_x) * (398/1280))
            dif_y = round(abs(center_y - tar_y) * (107/360))

            distance = math.sqrt(dif_x^2 + dif_y^2)
            print(distance)

        # 結果表示
        cv2.imshow('Frame', resultImg)
        cv2.imshow("Mask", mask)

        #保存
        #writer.write(resultImg)
        
        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    #保存
    cap.release()
    cv2.destroyAllWindows()
    #writer.release()

if __name__ == '__main__':
    main()
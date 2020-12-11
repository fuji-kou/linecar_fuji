import numpy as np
import math
import cv2
from experiment_settings2 import camera
import csv

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
    data = []

    real_distance_list = []
    distance = 111111

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


            area1 = target['area1']       #赤の面積
            area1 = area1/(1280*720)*100      #割合
            area1 = round(159.55*area1**(-0.525))
            real_distance_list.append(area1)
            
        # 結果表示
        cv2.imshow('Frame', resultImg)
        cv2.imshow("Mask", mask)
        
        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    #保存
    with open(f"C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\measurement\\data_{distance}.csv", 'w') as f:
        writer = csv.writer(f, lineterminator = '\n')
        for i in range(len(real_distance_list)):
            writer.writerows([[real_distance_list[i]]])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
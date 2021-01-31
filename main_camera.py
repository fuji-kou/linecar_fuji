import numpy as np
import math
import csv
import socket
import cv2
from camera_settings import camera

import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl

#カメラキャプチャ
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

TMP_FOLDER_PATH = "./cali/tmp/"
MTX_PATH = TMP_FOLDER_PATH + "mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "dist2.csv"

#FPS,解像度の設定
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def camera_measurement():
    ret, frame = cap.read()
    center_x = 640
    center_y = 360
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

        if target["center1"] == None:
            tar_x1 = None
            tar_y1 = None       
            distance_left = None
            difference_left = None
        else:
            tar_x1 = int(target["center1"][0])
            tar_y1 = int(target["center1"][1])
            (area1, area2) = (target['area1'], None)       #赤の面積
            (area1, area2) = (area1/(1280*720)*100, None)       #割合
            (area1, area2) = (round(159.55*area1**(-0.525)), None) #10-780
            distance_left = area1
            difference_left = center_x - tar_x1

        if target["center2"] == None:
            tar_x2 = None
            tar_y2 = None       
            distance_right = None
            difference_right = None
        else:
            tar_x2 = int(target["center2"][0])
            tar_y2 = int(target["center2"][1])
            (area1, area2) = (area1, target['area2'])       #赤の面積
            (area1, area2) = (area1, area2/(1280*720)*100)       #割合
            (area1, area2) = (area1, round(159.55*area2**(-0.525))) #10-780
            distance_right = area2
            difference_right = tar_x2 - center_x
        #フレームに面積最大ブロブの中心周囲を円で描く

    #表示
    #cv2.imshow('Frame', resultImg)
    return distance_left , distance_right , tar_x1 , tar_x2 , difference_left , difference_right


def main():
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
                angle1 = m1.controller.get_input_angle(now_latlon)
                distance_left,distance_right,tar_x1,tar_x2,difference_left,difference_right = camera_measurement()
                if difference_left == None or difference_right == None:
                    m1.mv_wheel(0)
                    m1.mv_angle(0)
                    
                else:
                    if tar_x1 <= 640 and tar_x2 <= 640:
                        angle = (tar_x2 - tar_x1)/2 -640
                        angle = angle*6400/(2*math.pi)
                        angle = angle*0.0001
                        type_area = "left_side"
                        print(angle,"left_side")
                    elif tar_x1 > 640 and tar_x2 > 640:
                        angle =  (tar_x2 - tar_x1)/2 - 640
                        angle = angle*6400/(2*math.pi)
                        angle = angle*0.0001
                        type_area = "rught_side"
                        print(angle,"right_side")
                    else:
                        if difference_left > difference_right:
                            angle = difference_left - difference_right

                            angle = angle*6400/(2*math.pi)
                            angle = angle*0.001
                            angle = -1*angle
                            type_area = "left"
                            print(angle,"left")
                        if difference_left == difference_right:
                            angle = 0
                            type_area = "="
                            print(angle,"=")
                        if difference_left < difference_right:
                            angle = difference_right - difference_left

                            angle = angle*6400/(2*math.pi)
                            angle = angle*0.001
                            type_area = "right"
                            print(angle,"right")
                    m1.mv_angle(angle)
                    record.append(m1.get_status())
                    #camera_record.append(tar_x1,tar_x2,angle,type_area)
                    #record = record + camera_record
                    #floutのとき
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

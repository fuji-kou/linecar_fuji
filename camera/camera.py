import cv2
import numpy as np
import datetime as dt
import sys
from time import sleep
from camera_settings import camera

TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
MTX_PATH = TMP_FOLDER_PATH + "\\mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "\\dist2.csv"

cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

#FPS,解像度の設定
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# #保存
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 10.0
size = (1280, 720)
SAVE_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\video\\"
now = dt.datetime.now()
time = now.strftime('%Y%m%d_%H%M_%S')
writer = cv2.VideoWriter(SAVE_PATH + 'video_{}.mp4'.format(time), fmt, fps, size)
 
while True:
    ret, frame = cap.read()
    mtx, dist = camera.loadCalibrationFile(MTX_PATH, DIST_PATH)         #キャリブレーションファイルの読み込み
    resultImg = cv2.undistort(frame, mtx, dist, None)
    cv2.imshow('Filter Frame', resultImg)
    writer.write(resultImg)     #保存

    #qキーで終了
    if cv2.waitKey(1) == ord('q'):
        break
 
#保存
writer.release()
cap.release()
cv2.destroyAllWindows()
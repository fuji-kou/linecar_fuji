import cv2
import numpy as np
import datetime as dt
import sys
sys.path.append("C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\")
import calibrate as cali

 
#cali.calibrateImage() 
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
 
#保存
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 60.0
size = (1280, 720)

SAVE_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\camera\\"


now = dt.datetime.now()
time = now.strftime('%Y%m%d_%H%M_%S')
writer = cv2.VideoWriter(SAVE_PATH + 'video_{}.mp4'.format(time), fmt, fps, size)
 
while True:
    ret, frame = cap.read()
    print(ret)                          #ret:フレームを取得できたかTrueかFalseで示す
    frame = cv2.resize(frame, size)
     
    #保存
    writer.write(frame)
     
    cv2.imshow('frame', frame)
    #qキーで終了
    if cv2.waitKey(1) == ord('q'):
        break
 
#保存
writer.release()
cap.release()
cv2.destroyAllWindows()
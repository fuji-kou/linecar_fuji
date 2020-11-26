import cv2
import numpy as np
import datetime as dt
import sys
sys.path.append("C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\")
import calibrate as cali

 
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
#cali.calibrateImage()
 
#保存
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 60.0
size = (1280, 720)

SAVE_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\camera\\"


now = dt.datetime.now()
time = now.strftime('%Y%m%d_%H%M_%S')
writer = cv2.VideoWriter(SAVE_PATH + 'video_{}.mp4'.format(time), fmt, fps, size)
 
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, size)
     
    #保存
    writer.write(frame)
     
    cv2.imshow('frame', frame)
    #Enterキーで終了
    if cv2.waitKey(1) == ord('q'):
        break
 
#保存
writer.release()
cap.release()
cv2.destroyAllWindows()
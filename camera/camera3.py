import cv2
import numpy as np
import datetime as dt
 
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
 
#保存
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 60.0
size = (1280, 720)


now = dt.datetime.now()
time = now.strftime('%Y%m%d-%H%M%S')
writer = cv2.VideoWriter('data/camera/video_{}.mp4'.format(time), fmt, fps, size)
 
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
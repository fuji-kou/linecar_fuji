import cv2
import datetime as dt
import sys

cap = cv2.VideoCapture("C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\video\\" + 'video_20201127_1824_08.mp4')

delay = 1
window_name = 'frame'


while True:
    ret, frame = cap.read()
    print(ret)
    if ret:
        cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        cap.set(cv2.CAP_PROP_POSqq_FRAMES, 0)

cv2.destroyWindow(window_name)
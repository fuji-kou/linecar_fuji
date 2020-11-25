import cv2
import numpy as np
import datetime

camera = cv2.VideoCapture(0+cv2.CAP_DSHOW)
print(type(camera))
# <class 'cv2.VideoCapture'>
print(camera.isOpened())
# True

#FPS,解像度の設定
camera.set(cv2.CAP_PROP_FPS, 60)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))


#動画ファイル保存用の設定
fps = int(camera.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用)
#now = datetime.datetime.now()
#filename = 'camera_log' + now.strftime('%Y%m%d_%H%M%S') + '.mp4'
#f = open(filename, 'w')
#writer = writer(f, lineterminator='\n') 
video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

 
# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    ret, frame = camera.read()              # フレームを取得
    cv2.imshow('camera', frame)             # フレームを画面に表示
    video.write(frame)                      # 動画を1フレームずつ保存する
 
    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video.write(frame)                      # 動画を1フレームずつ保存する
        break
 
# 撮影用オブジェクトとウィンドウの解放
camera.release()
video.release()
cv2.destroyAllWindows()
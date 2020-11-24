import cv2

cap_cam = cv2.VideoCapture(0+cv2.CAP_DSHOW)
print(type(cap_cam))
# <class 'cv2.VideoCapture'>

print(cap_cam.isOpened())
# True

 
# 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    ret, frame = cap_cam.read()              # フレームを取得
    cv2.imshow('cap_cam', frame)             # フレームを画面に表示
 
    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# 撮影用オブジェクトとウィンドウの解放
cap_cam.release()
cv2.destroyAllWindows()
import numpy as np
import cv2
import glob
from time import sleep
from datetime import datetime

TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
MTX_PATH = TMP_FOLDER_PATH + "\\mtx.csv"
DIST_PATH = TMP_FOLDER_PATH + "\\dist.csv"

cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

#FPS,解像度の設定
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# キャリブレーションCSVファイルを読み込む関数
def loadCalibrationFile(mtx_path, dist_path):
  try:
      mtx = np.loadtxt(mtx_path, delimiter=',')
      dist = np.loadtxt(dist_path, delimiter=',')
  except Exception as e:
      raise e
  return mtx, dist


while True:
  ret, frame = cap.read()
  # 1/2サイズに縮小
  #frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
  # 無修正画像を表示
  #cv2.imshow('Raw Frame', frame)

  #内部パラメータを元に画像補正
  mtx, dist = loadCalibrationFile(MTX_PATH, DIST_PATH)
  resultImg = cv2.undistort(frame, mtx, dist, None)
  #saveImgByTime(SAVE_FOLDER_PATH, resultImg)
  cv2.imshow('Filter Frame', resultImg)

  if cv2.waitKey(1) == ord('q'):
    break  


# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
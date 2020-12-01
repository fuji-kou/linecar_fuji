import numpy as np
import cv2
import glob
#from time import sleep
import time
import datetime as dt
import os

#カメラキャプチャ
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
MTX_PATH = TMP_FOLDER_PATH + "\\mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "\\dist2.csv"

#FPS,解像度の設定
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # #保存
# fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# fps = 10.0
# size = (1280, 720)
# SAVE_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\video\\"
# now = dt.datetime.now()
# time = now.strftime('%Y_%m%d_%H%M_%S')
# writer = cv2.VideoWriter(SAVE_PATH + 'video_{}.mp4'.format(time), fmt, fps, size)

# キャリブレーションCSVファイルを読み込む関数
def loadCalibrationFile(mtx_path, dist_path):
  try:
      mtx = np.loadtxt(mtx_path, delimiter=',')
      dist = np.loadtxt(dist_path, delimiter=',')
  except Exception as e:
      raise e
  return mtx, dist

# # 画像を時刻で保存する関数
# def saveImgByTime(dirPath, img):
#     # 時刻を取得
#     date = datetime.now().strftime("%Y_%m%d_%S")
#     path = dirPath + date + ".jpg"
#     cv2.imwrite(path, img) # ファイル保存
#     print("saved: ", path)

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,185,0])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,127,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    
    return mask1 + mask2

# ブロブ解析
def analysis_blob(binary_img):
    # 2値画像のラベリング処理
    label = cv2.connectedComponentsWithStats(binary_img)

    # ブロブ情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # ブロブ面積最大のインデックス
    max_index = np.argmax(data[:, 4])

    # 面積最大ブロブの情報格納用
    maxblob = {}

    # 面積最大ブロブの各種情報を取得
    maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    maxblob["width"] = data[:, 2][max_index]  # 幅
    maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]   # 面積
    maxblob["center"] = center[max_index]  # 中心座標
    
    
    return maxblob

def main():    
     # データ格納用のリスト
    data = []

    # 記録データの保存先パス
    #csvfile_path = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\tracking"
    # 開始時間
    start = time.time()

    while(cap.isOpened()):
        ret, frame = cap.read()
        #キャリブレーション適用
        mtx, dist = loadCalibrationFile(MTX_PATH, DIST_PATH)
        resultImg = cv2.undistort(frame, mtx, dist, None)
 
        #赤色検出
        mask = red_detect(resultImg)

        #マスク画像をブロブ解析（面積最大のブロブ情報を取得）
        target = analysis_blob(mask)

        #面積最大ブロブの中心座標を取得
        center_x = int(target["center"][0])
        center_y = int(target["center"][1])
        #print(center_x , center_y)
        # フレームに面積最大ブロブの中心周囲を円で描く
        cv2.circle(resultImg, (center_x, center_y), 30, (0, 200, 0),
                   thickness=3, lineType=cv2.LINE_AA)
        
        

        # 結果表示
        cv2.imshow('Frame', resultImg)
        cv2.imshow("Mask", mask)

        #保存
        #writer.write(mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    #保存
    cap.release()
    cv2.destroyAllWindows()
    #writer.release()

if __name__ == '__main__':
    main()
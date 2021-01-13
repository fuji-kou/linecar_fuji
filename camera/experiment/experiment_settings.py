import numpy as np
import cv2
import datetime as dt

TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
MTX_PATH = TMP_FOLDER_PATH + "\\mtx2.csv"
DIST_PATH = TMP_FOLDER_PATH + "\\dist2.csv"

class camera():
    # キャリブレーションCSVファイルを読み込む関数
    def loadCalibrationFile(mtx_path, dist_path):
        try:
            mtx = np.loadtxt(mtx_path, delimiter=',')
            dist = np.loadtxt(dist_path, delimiter=',')
        except Exception as e:
            raise e
        return mtx, dist

    # 画像を時刻で保存する関数
    def saveImgByTime(dirPath, img):
        # 時刻を取得
        date = datetime.now().strftime("%Y_%m%d_%S")
        path = dirPath + date + ".jpg"
        cv2.imwrite(path, img) # ファイル保存
        print("saved: ", path)

    def red_detect(img):
        # HSV色空間に変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 赤色のHSVの値域1
        hsv_min = np.array([0,100,0])
        hsv_max = np.array([15,255,255])
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

        # 赤色のHSVの値域2
        hsv_min = np.array([165,100,0])
        hsv_max = np.array([180,255,255])
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



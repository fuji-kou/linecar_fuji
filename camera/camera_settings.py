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
        #print(data)
        center = np.delete(label[3], 0, 0)

        # ブロブ面積最大のインデックス
        max_index = np.argmax(data[:, 4])
        #print(max_index)
        #print(data[max_index][4])
        #data2 = sorted(data, key=lambda x :x[4])
        #pprint.pprint(data2[-1][4])


        # 面積最大ブロブの情報格納用
        maxblob = {}

        # 面積最大ブロブの各種情報を取得
        maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
        maxblob["width"] = data[:, 2][max_index]  # 幅
        maxblob["height"] = data[:, 3][max_index]  # 高さ
        maxblob["area"] = data[:, 4][max_index]   # 面積
        maxblob["center"] = center[max_index]  # 中心座標
        # print(maxblob)
        # if len(data2) == 0:
        #     # pass
        
        # if len(data2) == 1:
        #     #camera1
        #     maxblob["upper_left1"] = (data2[-1][0], data2[-1][1]) # 左上座標
        #     maxblob["width1"] = data2[-1][2]  # 幅
        #     maxblob["height1"] = data2[-1][3]  # 高さ
        #     maxblob["area1"] = data2[-1][4]   # 面積
        #     maxblob["center1"] = (data2[-1][0]+data2[-1][2]/2,data2[-1][1]+data2[-1][3]/2)  # 中心座標

        #     #camera2
        #     maxblob["upper_left2"] = (0,0)# 左上座標
        #     maxblob["width2"] = 0  # 幅
        #     maxblob["height2"] = 0  # 高さ
        #     maxblob["area2"] = 0   # 面積
        #     maxblob["center2"] = (0,0)
     
        # else:
        #     #camera1
        #     maxblob["upper_left1"] = (data2[-1][0], data2[-1][1]) # 左上座標
        #     maxblob["width1"] = data2[-1][2]  # 幅
        #     maxblob["height1"] = data2[-1][3]  # 高さ
        #     maxblob["area1"] = data2[-1][4]   # 面積
        #     maxblob["center1"] = (data2[-1][0]+data2[-1][2]/2,data2[-1][1]+data2[-1][3]/2)  # 中心座標

        #     #camera2
        #     maxblob["upper_left2"] = (data2[-2][0], data2[-2][1]) # 左上座標
        #     maxblob["width2"] = data2[-2][2]  # 幅
        #     maxblob["height2"] = data2[-2][3]  # 高さ
        #     maxblob["area2"] = data2[-2][4]   # 面積
        #     maxblob["center2"] = (data2[-2][0]+data2[-2][2]/2,data2[-2][1]+data2[-2][3]/2)  # 中心座標

        #     # print(maxblob)
            
        return maxblob



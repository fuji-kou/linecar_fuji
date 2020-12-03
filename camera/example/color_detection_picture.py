import numpy as np
import cv2
import glob
from time import sleep
from datetime import datetime
import os


SAVE_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\color_result\\"
# 画像を時刻で保存する関数
def saveImgByTime(dirPath, img):
    # 時刻を取得
    date = datetime.now().strftime("%Y_%m%d_%S")
    path = dirPath + date + ".jpg"
    cv2.imwrite(path, img) # ファイル保存
    print("saved: ", path)

# 赤色の検出
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,185,50])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,64,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色領域のマスク（255：赤色、0：赤色以外）    
    mask = mask1 + mask2

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 緑色の検出
def detect_green_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    hsv_min = np.array([30, 64, 0])
    hsv_max = np.array([90,255,255])

    # 緑色領域のマスク（255：赤色、0：赤色以外）    
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    
    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

# 青色の検出
def detect_blue_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青色のHSVの値域1
    hsv_min = np.array([90, 64, 0])
    hsv_max = np.array([150,255,255])

    # 青色領域のマスク（255：赤色、0：赤色以外）    
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img



# 入力画像の読み込み
files = glob.glob("C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\color_img\\*.jpg")

for fn in files:
    img = cv2.imread(fn)

    # 色検出（赤、緑、青）
    red_mask, red_masked_img = detect_red_color(img)
    green_mask, green_masked_img = detect_green_color(img)
    blue_mask, blue_masked_img = detect_blue_color(img)


    # 結果を出力
    saveImgByTime(SAVE_FOLDER_PATH + 'red_mask_', red_mask)
    saveImgByTime(SAVE_FOLDER_PATH + 'red_masked_', red_masked_img)
    saveImgByTime(SAVE_FOLDER_PATH + 'green_mask_', green_mask)
    saveImgByTime(SAVE_FOLDER_PATH + 'green_masked_', green_masked_img)
    saveImgByTime(SAVE_FOLDER_PATH + 'blue_mask_', blue_mask)
    saveImgByTime(SAVE_FOLDER_PATH + 'blue_masked_', blue_masked_img)

    sleep(1)
import numpy as np
import math
import csv
import socket
import cv2
from camera_settings import camera


def camera_measurement(ret, frame):
    TMP_FOLDER_PATH = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali\\tmp"
    MTX_PATH = TMP_FOLDER_PATH + "\\mtx2.csv"
    DIST_PATH = TMP_FOLDER_PATH + "\\dist2.csv"
    center_x = 640
    center_y = 360
    #キャリブレーション適用
    mtx, dist = camera.loadCalibrationFile(MTX_PATH, DIST_PATH)
    resultImg = cv2.undistort(frame, mtx, dist, None)
    #赤色検出
    mask = camera.red_detect(resultImg)
    w, h = mask.shape
    empty_image = np.zeros((w,h), dtype = np.uint8)
    dif = mask - empty_image
    if dif.any() == 0:      #零行列の場合
        pass

    else:
        #マスク画像をブロブ解析（面積最大のブロブ情報を取得）
        target = camera.analysis_blob(mask)

        if target["center1"] == None:
            tar_x1 = None
            tar_y1 = None       
            distance_left = None
            difference_left = None
        else:
            tar_x1 = int(target["center1"][0])
            tar_y1 = int(target["center1"][1])
            (area1, area2) = (target['area1'], None)       #赤の面積
            (area1, area2) = (area1/(1280*720)*100, None)       #割合
            (area1, area2) = (round(159.55*area1**(-0.525)), None) #10-780
            distance_left = area1
            difference_left = center_x - tar_x1

        if target["center2"] == None:
            tar_x2 = None
            tar_y2 = None       
            distance_right = None
            difference_right = None
        else:
            tar_x2 = int(target["center2"][0])
            tar_y2 = int(target["center2"][1])
            (area1, area2) = (area1, target['area2'])       #赤の面積
            (area1, area2) = (area1, area2/(1280*720)*100)       #割合
            (area1, area2) = (area1, round(159.55*area2**(-0.525))) #10-780
            distance_right = area2
            difference_right = tar_x2 - center_x
        #フレームに面積最大ブロブの中心周囲を円で描く

    #表示
    #cv2.imshow('Frame', resultImg)
    return distance_left , distance_right , tar_x1 , tar_x2 , difference_left , difference_right
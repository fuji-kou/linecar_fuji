import numpy as np
import math
import csv
import socket
import cv2

def order_fix(distance_left, tar_x1):
    if distance_left == None:
        left_order = 'Stop'
    else:
        if distance_left >= 120:
            if tar_x1 == 375:
                left_order = 'GO'
            elif tar_x1 < 250:
                left_order = 'turn_left1'
            elif 250 < tar_x1 < 375:
                left_order = 'turn_left2'
            elif tar_x1 > 500:
                left_order = 'turn_right1'
            elif 375 < tar_x1 <= 500:
                left_order = 'turn_right2'
        else:
            left_order = 'Stop'
    return left_order

def order_float(distance_left, tar_x1):
    if difference_left == None:
        pass
    else:
        if distance_left >= 400:
            if tar_x1 == 375:
                left_order = 'GO'
            elif tar_x1 < 250:
                left_order = 'turn_left1'
            elif 250 <= tar_x1 < 375:
                left_order = 'turn_left2'
            elif tar_x1 > 500:
                left_order = 'turn_right1'
            elif 375 < tar_x1 <= 500:
                left_order = 'turn_right2'
        else:
            left_order = 'Stop'
    return left_order
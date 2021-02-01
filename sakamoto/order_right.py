import numpy as np
import math
import csv
import socket
import cv2

def order_fix(distance_right, tar_x2):
    if distance_right == None:
        right_order = 'Stop'
    else:
        if distance_right >= 120:
            if tar_x2 == 905:
                right_order = 'GO'
            elif tar_x2 < 780:
                right_order = 'turn_left1'
            elif 780 < tar_x2 < 905:
                right_order = 'turn_left2'
            elif tar_x2 > 1030:
                right_order = 'turn_right1'
            elif 905 < tar_x2 <= 1030:
                right_order = 'turn_right2'
        else:
            right_order = 'Stop'
    return right_order

def order_float(distance_right, tar_x2):
    if difference_right == None:
        pass
    else:
        if distance_right >= 400:
            if tar_x2 == 905:
                right_order = 'GO'
            elif tar_x2 < 780:
                right_order = 'turn_left1'
            elif 780 <= tar_x2 < 905:
                right_order = 'turn_left2'
            elif tar_x2 > 1030:
                right_order = 'turn_right1'
            elif 905 < tar_x2 <= 1030:
                right_order = 'turn_right2'
        else:
            right_order = 'Stop'
    return right_order
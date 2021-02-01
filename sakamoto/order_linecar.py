import numpy as np
import math
import csv
import socket
import cv2

type_area = '='
def order_float(tar_x1, tar_x2, difference_left, difference_right):
    if difference_left == None or difference_right == None:
        m1.mv_wheel(0)
        m1.mv_angle(0)
        
    else:
        if tar_x1 <= 640 and tar_x2 <= 640:
            angle = (tar_x2 - tar_x1)/2 -640
            angle = angle*6400/(2*math.pi)
            angle = angle*0.0001
            type_area = "left_side"
            print(angle,"left_side")
        elif tar_x1 > 640 and tar_x2 > 640:
            angle =  (tar_x2 - tar_x1)/2 - 640
            angle = angle*6400/(2*math.pi)
            angle = angle*0.0001
            type_area = "rught_side"
            print(angle,"right_side")
        else:
            if difference_left > difference_right:
                angle = difference_left - difference_right
    
                angle = angle*6400/(2*math.pi)
                angle = angle*0.001
                angle = -1*angle
                type_area = "left"
                print(angle,"left")
            if difference_left == difference_right:
                angle = 0
                type_area = "="
                print(angle,"=")
            if difference_left < difference_right:
                angle = difference_right - difference_left
    
                angle = angle*6400/(2*math.pi)
                angle = angle*0.001
                type_area = "right"
                print(angle,"right")
    return angle, type_area   
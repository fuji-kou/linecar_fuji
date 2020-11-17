import os
import sys
import math

sys.path.append('../')
import linecar_settings as sets
from .Control import Control


class PurePursuitControl(Control):
    def __init__(self):
        self.K = sets.K
        self.Lfc = sets.Lfc

        self.reference_point = None
        self.target_course_x = None
        self.target_course_y = None

        self.pind = None
        self.nearest_point_index = None

    def prepare(self):
        self.reference_point = sets.REFERENCE_POINT
        self.target_course_x = sets.TARGET_X
        self.target_course_y = sets.TARGET_Y

        #実機の方位
        

    def get_input_angle(self, current_position, vc, w_theta):
        xy = self.latlon2xy(current_position)
        i = self.calc_target_index(current_position, vc)
        d2target = self.calc_distance_to_target(xy, i)

        if self.pind >= i:
            i = self.pind
        if i < len(self.target_course_x):
            tx = self.target_course_x[i]
            ty = self.target_course_y[i]
        else:
            tx = self.target_course_x[-1]
            ty = self.target_course_y[-1]
            i = len(self.target_course_x) - 1
        # self.wld_thetaは実機では不明な値．
        alpha = math.atan2(ty-xy[1], tx-xy[0]) - w_theta
        input_angle = math.atan2(2*sets.WHEELBASE*math.sin(alpha), d2target)
        input_angle = self.rad2mil(input_angle)

        return input_angle

    def calc_distance_to_target(self, xy, index):
        dx = xy[0] - self.target_course_x[index]
        dy = xy[1] - self.target_course_y[index]
        distance = math.sqrt(dx**2 + dy**2)

        return distance

    def calc_target_index(self, current_position, vc):
        xy = self.latlon2xy(current_position)
        if self.nearest_point_index is None:
            # search nearest point index
            dx = [xy[0] - icx for icx in self.target_course_x]
            dy = [xy[1] - icy for icy in self.target_course_y]
            d = [math.sqrt(idx**2 + idy**2) for (idx, idy) in zip(dx, dy)]
            i = d.index(min(d))
            self.nearest_point_index = i
        else:
            i = self.nearest_point_index
            d2nearest = self.calc_distance_to_target(xy, i)
            while True:
                i = i + 1 if (i+1)<len(self.target_course_x) else i
                d2target = self.calc_distance_to_target(xy, i)
                if d2nearest < d2target:
                    break
                d2nearest = d2target
                self.nearest_point_index = i
        L = 0
        Lf = self.K*vc + self.Lfc
        # search look ahead target point index
        while Lf > L and (i+1)<len(self.target_course_x):
            L = self.calc_distance_to_target(xy, i)
            i += 1

        if self.pind is None:
            self.pind = i
        
        return i

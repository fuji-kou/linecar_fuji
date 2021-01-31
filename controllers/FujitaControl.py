import os
import sys
import math

sys.path.append('../')
import linecar_settings as sets
from .Control import Control


class FujitaControl(Control):
    def __init__(self):
        self.reference_point = sets.REFERENCE_POINT
        self.start_point = sets.POSITION_START

        self.distance_s2g = None
        self.theta_s2g = None

        self.distance_s2r = None
        self.theta_s2r = None
        self.theta_diff = None
        self.side_diff = None

        self.input_angle = None
    
    def prepare(self):
        """最初一回だけ行う処理．スタートからゴールへの距離と方位を計算する．
        """        
        self.distance_s2g, self.theta_s2g = self.calc_distance_direction(self.start_point, sets.POSITION_END)

    def get_input_angle(self, current_position):
        """内部変数を更新しつつ入力舵角を返す．
        
        Arguments:
            current_position {[float]} -- lat, lon[deg]
        
        Returns:
            input_angle[float] -- 入力舵角[mil]
        """        
        self.distance_s2r, self.theta_s2r = self.calc_distance_direction(self.start_point, current_position)
        self.theta_diff = self.theta_s2r - self.theta_s2g
        self.side_diff = math.tan(self.theta_diff)*self.distance_s2r*1000
        self.input_angle = -1 * sets.GAIN_FJT * self.side_diff

        return self.input_angle
    
    def is_finished(self):
#         """終了判定はコントローラに依存すると思うのでこちらに
#         
#         Returns:
#             [bool] -- 終わってたらTrueを返す．
#         """
        return self.distance_s2r > 7



    def get_internal_variables(self):
        """この操舵メソッドの内部変数を返す．
        
        Returns:
            iv{[float]} -- 内部変数．
        """        
        iv = [self.input_angle, self.distance_s2r, self.theta_diff, self.side_diff]

        return iv

    def calc_distance_direction(self, start, end):
        start_xy = self.latlon2xy(start)
        end_xy = self.latlon2xy(end)

        dlt_x = end_xy[0] - start_xy[0]
        dlt_y = end_xy[1] - start_xy[1]
        distance = math.sqrt(dlt_x**2 + dlt_y**2)
        theta = math.atan2(dlt_y, dlt_x)

        return [distance, theta]

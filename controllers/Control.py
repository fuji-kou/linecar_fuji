import os
import sys
import math
from abc import ABCMeta, abstractmethod

sys.path.append('../')
import linecar_settings as sets


class Control(metaclass=ABCMeta):
    def __init__(self):
        self.reference_point = sets.REFERENCE_POINT

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def get_input_angle(self):
        pass

    @abstractmethod
    def is_finished(self):
        pass

    @abstractmethod
    def get_internal_variables(self):
        pass

    def latlon2xy(self, latlon):
        """緯度・経度の値をself.REFERENCE_POINTを基準にしたx-y座標に変換する．

        Args:
            latlon (float): 緯度・経度　(lat, lon)[deg]

        Returns:
            xy (float): x-y座標（x, y) [m]

        """
        L = 111319.4908
        lat_refp, lon_refp = self.reference_point
        y = (latlon[0] - lat_refp) * L
        x = (latlon[1] - lon_refp) * L * math.cos(math.radians(lat_refp))

        return [x, y]
    
    def xy2latlon(self, xy):
        """self.REFERENCE_POINTを基準にしたx-y座標の値を緯度・経度の値に変換する．

        Args:
            xy (float): x-y座標（x, y) [m]

        Returns:
            latlon (float): 緯度・経度　(lat, lon)[deg]

        """
        L = 111319.4908
        lat_refp, lon_refp = self.reference_point
        lat = xy[1]/L + lat_refp
        lon = xy[0]/(L*math.cos(math.radians(lat_refp))) + lon_refp

        return [lat, lon]
    
    @staticmethod
    def rad2mil(rad):
        """角度の単位を[rad]から[mil]に変換する．

        Args:
            input_angle (float): 角度[rad]

        Returns:
            output_angle (float): 角度[mil]

        """
        mil = rad*6400/(2*math.pi)

        return mil

    @staticmethod
    def mil2rad(mil):
        """角度の単位を[mil]から[rad]に変換する．

        Args:
            input_angle (float): 角度[mil]

        Returns:
            output_angle (float): 角度[rad]

        """
        rad = (2*math.pi/6400) * mil

        return rad

import math
import numpy as np
import serial
import socket
import time

from io import StringIO

import linecar_settings as sets
from controllers.FujitaControl import FujitaControl
from controllers.PurePursuitControl import PurePursuitControl
from controllers.FixedAngleTestControl import FixedAngleTestControl


class LineCar(object):
    def __init__(self):
        self.REFERENCE_POINT = sets.REFERENCE_POINT
        self.gpsinfo = None
        # Select control method.
        self.controller = FujitaControl()
        # USB
        self.serial = None
        self.socket = None

    def setup4experiment(self):
        """実験用のセットアップを行う．
        """        
        self.serial_start()
        self.socket_start()
        self.init_steering_angle()
    
    def setup4movement(self):
        """移動用のセットアップを行う．
        """        
        self.serial_start()
        self.init_steering_angle()

    def serial_start(self):
        """本体とのシリアル通信を始める．
        """        
        self.serial = serial.Serial(sets.COM_PORT, sets.BAUDRATE, timeout=sets.TIMEOUT)
        time.sleep(3)

    def socket_start(self):
        """GPSのデータ取得に使うソケットを開く．
        """        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((sets.ADDRESS, sets.PORT_NUM))
        except ConnectionRefusedError:
            self.socket = None

    def init_steering_angle(self):
        """舵角センサー調整の儀式．
        """        
        self.serial.write(b'w0\nt0\n')
        angle = self.get_current_angle()
        command = 't{0}\n'.format(-1*angle).encode()
        self.serial.write(command)
        angle = self.get_current_angle()

    def stop(self):
        """終了処理
        """        
        self.mv_wheel(0)
        if self.serial is not None:
            self.serial.close()
        if self.socket is not None:
            self.socket.close()

    def mv_wheel(self, velocity):
        """ラインカーに目標速度を送信する．
        
        Arguments:
            velocity {[float]} -- 速度の入力値．[cm/s]
        """        
        command = 'v{0}\n'.format(velocity).encode()
        self.serial.write(command)

    def mv_angle(self, angle):
        """ラインカーに目標舵角を送信する．

        Arguments:
            angle {[float]} -- 舵角の入力値．[mil]
        """        
        command = 'a{0}\n'.format(angle).encode()
        self.serial.write(command)

    def get_current_angle(self):
        """ラインカーから現在の舵角を教えてもらう．
        
        Returns:
            current_angle[int] -- ラインカーの現在の舵角．[mil]
        """
        self.serial.write(b'a?\n')
        while True:
            res = self.serial.readline().decode()
            if 'A=' in res:
                res = res.split(' ')[0]
                res = res.lstrip('A=').rstrip('mil')
                current_angle = int(res)
                break      
        return current_angle

    def get_current_position(self):
        """現在地を取得する．

        get_gpsinfo()の返す値のうちlat/lonだけをfloatで返す．
        
        Returns:
            {[float]} -- lat, lon
        """        
        self.gpsinfo = self._get_gpsinfo()
        current_position = [float(self.gpsinfo[2]), float(self.gpsinfo[3]),int(self.gpsinfo[5])]

        return current_position

    def _get_gpsinfo(self):
        # TODO; 実機と通信しながらデバッグ
        """socketを介してRTK-GPSのデータを取得する．

        外からは呼ばない（予定）
        
        Returns:
            dlist{[str]} -- GPS関連の全部で15個の数値．
        """        
        if self.socket is None:
            dlist = ['0' for i in range(1,15)]
        else:
            buff = StringIO()
            data = self.socket.recv(sets.BUFSIZE)
            buff.write(data.decode('utf-8'))
            data = buff.getvalue().replace('b',"")
            print(data)
            dlist = data.split()
            buff.close()
            # dlistは day, timing, ns, nw_lat, nw_lon, statusを含んだlist(たぶんね)
        return dlist

    def get_status(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """        
        status = self.gpsinfo[0:7]
        cur_angle = self.get_current_angle()
        ctrl_iv = self.controller.get_internal_variables()

        status.append(cur_angle)
        status = status + ctrl_iv

        return status

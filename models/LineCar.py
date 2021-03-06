import math
import numpy as np
import serial
import socket
import time
from time import sleep
import sys
from io import StringIO

sys.path.append('../')
import linecar_settings as sets
from controllers.FujitaControl import FujitaControl

#ラズパイ
import RPi.GPIO as GPIO     
from time import sleep

class LineCar(object):    
    def __init__(self):
        self.REFERENCE_POINT = sets.REFERENCE_POINT
        self.gpsinfo = None
        # Select control method.
        self.controller = FujitaControl()
        # USB
        self.socket = None
#         #　GPIOの設定   
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)
#         #　サーボモータ,モータのピンの設定
#         Servo_pin = 18
#         pwm = 23                           #pwmピンを23に設定
#         DIR = 24                           #DIRピンを24に設定
#         GPIO.setup(Servo_pin, GPIO.OUT)
#         GPIO.setup(pwm, GPIO.OUT)      #出力設定          
#         GPIO.setup(DIR, GPIO.OUT) 
#         #　PWMの設定:GPIO.PWM(ポート番号, 周波数[Hz])
#         self.Servo = GPIO.PWM(Servo_pin, 50)
#         self.p1 = GPIO.PWM(pwm, 100)            
#         #　パルス出力開始。　servo.start( [デューティサイクル 0~100%] )とりあえずゼロ指定だとサイクルが生まれないので特に動かない？
#         self.Servo.start(0)
        
    # 実験用のセットアップ(ok)
    def setup4experiment(self):
        self.socket_start()
        # self.init_steering_angle()

#     # 移動用のセットアップ(ok)
#     def setup4movement(self):   
#         self.init_steering_angle()

    # GPSのデータ取得に使うソケットを開く(ok)
    def socket_start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((sets.ADDRESS, sets.PORT_NUM))
        except ConnectionRefusedError:
            self.socket = None
            
#     # 舵角センサ調整儀式(ok?)
#     def init_steering_angle(self):
#         self.mv_angle(0)
            
    # #終了処理(ok)
    def stop(self):
        #GPIO.output(DIR, GPIO.LOW)
#         self.p1.start(0)
        if self.socket is not None:
            self.socket.close()
         
      # ラインカーに目標速度を送信(arduinoとの通信　直接指定すればok)   
#     def mv_wheel(self, velocity):
#         """
#         Arguments:
#             velocity {[float]} -- 速度の入力値．[cm/s]
#         """        
#         command = 'v{0}\n'.format(velocity).encode()
#         self.serial.write(command)
    
#     #現在のサーボの角度を返す
#     def currentdirection( self ):
#         return self.direction
  
#     # ラインカーに目標舵角を送信
#     def mv_angle(self, angle):    
#         duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180     # 角度からデューティ比を求める
#         self.Servo.ChangeDutyCycle(duty)                   # デューティ比を変更
#         time.sleep(0.3)
        
    def get_current_angle(self):
        


        return current_angle
#     def get_current_angle(self):
#         """ラインカーから現在の舵角を教えてもらう．
#         
#         Returns:
#             current_angle[int] -- ラインカーの現在の舵角．[mil]
#         """
#         self.serial.write(b'a?\n')
#         while True:
#             res = self.serial.readline().decode()
#             if 'A=' in res:
#                 res = res.split(' ')[0]
#                 res = res.lstrip('A=').rstrip('mil')
#                 current_angle = int(res)
#                 break      
#         return current_angle
    
    # 現在地を取得ok
    def get_current_position(self):
        """
        get_gpsinfo()の返す値のうちlat/lonだけをfloatで返す．
        
        Returns:
            {[float]} -- lat, lon
        """        
        self.gpsinfo = self._get_gpsinfo()
        current_position = [float(self.gpsinfo[2]), float(self.gpsinfo[3])]

        return current_position

    # socketを介してRTK-GPSのデータを取得ok
    def _get_gpsinfo(self):
        # TODO; 実機と通信しながらデバッグ
        """
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
        cur_angle = 1
        #self.get_current_angle()
        ctrl_iv = self.controller.get_internal_variables()

        status.append(cur_angle)
        status = status + ctrl_iv

        return status

import socket
from time import sleep
#import RPi.GPIO as GPIO
import sys
import os
# sys.path.append('..')
# import linecar_settings as sets

# servo
def mv_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)     #デューティ比を変更


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバを指定
#同端末
sock.connect(('127.0.0.1', 50007))
#ファーウェイタブ（ラズパイとの通信）
#s.connect(('192.168.43.198', 50007))
# サーバにメッセージを送る
while True:
    sock.sendall(b'connect')

        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = sock.recv(1024)

        
    if data == (b'start!!!!'):
        print(data)
        data = 0
    if data == 0:
        break











        #print(repr(data))
    #p1.start(sets.SPEED)
    # if data == (b'start!!!!'):
    #     print(b'Received: ' + data)




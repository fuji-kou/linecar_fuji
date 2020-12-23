import socket
from time import sleep
import RPi.GPIO as GPIO
import sys
import os
sys.path.append('..')
import linecar_settings as sets


# pin設定
GPIO.setmode(GPIO.BCM)      
GPIO.setwarnings(False)             #GPIOからの警告を有効にする

GPIO.setup(sets.pwm, GPIO.OUT)      #出力設定          
GPIO.setup(sets.DIR, GPIO.OUT)
GPIO.setup(sets.Servo_pin, GPIO.OUT)  
sleep(1)

p1 = GPIO.PWM(sets.pwm, 100)            #pwmピンの設定
Servo = GPIO.PWM(sets.Servo_pin, 50) 
Servo.start(0)                      

# servo
def mv_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)     #デューティ比を変更


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    #s.connect(('127.0.0.1', 50007))
    s.connect(('192.168.43.198', 50007))
    # サーバにメッセージを送る
    s.sendall(b'hello')
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = s.recv(1024)
    #
    print(repr(data))
    p1.start(10)
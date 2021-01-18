import socket
from time import sleep
import sys
import os
import RPi.GPIO as GPIO
# sys.path.append('..')
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


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバを指定
#同端末
#sock.connect(('127.0.0.1', 50007))
#ファーウェイタブ（ラズパイとの通信）
sock.connect(('192.168.43.198', 50007))
#実機パソコン
#sock.connect(('192.168.179.2', 50007))
#sock.connect(('192.168.11.34',50008))

# サーバにメッセージを送る
while True:
    sock.sendall(b'connect')

        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = sock.recv(1024)

        
    if data == (b'start!!!!'):
        print(data)
        #data = 0
    if data == (b'Go!!!!'):
        print(data)
        p1.start(10)
    if data == (b'Go'):
        print(data)
        p1.start(10)
    if data == (b'Stop!!!!'):
        print(data)
        p1.start(0)
    if data == (b'Stop'):
        print(data)
        p1.start(0)

    if data == 0:
        break











        #print(repr(data))
    #p1.start(sets.SPEED)
    # if data == (b'start!!!!'):
    #     print(b'Received: ' + data)




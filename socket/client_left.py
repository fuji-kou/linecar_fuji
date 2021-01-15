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
#ファーウェイタブ（ラズパイとの通信）my_PC
sock.connect(('192.168.43.198', 50007))
#実機パソコン
#sock.connect(('192.168.179.2', 50007))
#sock.connect(('192.168.11.34',50008))

#sock.connect(('192.168.11.12',50009))

# サーバにメッセージを送る
while True:
    sock.sendall(b'connect')

        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = sock.recv(1024)

    #開始・floutからの復帰  
    if data == (b'start!!'):
        print(data)
        mv_angle(0)
        p1.start(sets.SPEED)
        sleep(5)
    #離れすぎたら前に出る
    if data == (b'Go1'):
        print(data)
        mv_angle(0)
        p1.start(sets.SPEED)
    if data == (b'Go2'):
        pass
    #flout
    if data == (b'stop!!'):
        print(data)
        p1.start(0)
    #前出すぎたらストップ
    if data == (b'Stop1'):
        print(data)
        p1.start(0)
    if data == (b'Stop2'):
        pass
    #範囲から出たとき
    if data == (b'turn_left1'):
        mv_angle(20)
        p1.start(sets.turn_SPEED)
        sleep(5) 
    if data == (b'turn_left2'):
        pass
    #範囲から出たとき
    if data == (b'turn_right1'):
        mv_angle(-20)
        p1.start(sets.turn_SPEED)
        sleep(5)
    if data == (b'turn_right2'):
        pass

    if data == 0:
        mv_angle(0)
        break
















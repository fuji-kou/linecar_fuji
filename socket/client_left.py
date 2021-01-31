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
#sock.connect(('127.0.0.1', 50009))
#ファーウェイタブ（ラズパイとの通信）DELL
sock.connect(('192.168.43.198', 50006))

# サーバにメッセージを送る
while True:
    sock.sendall(b'connect')

        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = sock.recv(1024)

    #開始・floutからの復帰  
    if data == (b'start!!'):
        print(data)
        sleep(2)
        mv_angle(0)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.SPEED)
        
    #離れすぎたら前に出る
    if data == (b'Go'):
        print(data)
        #mv_angle(0)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.SPEED)
    #flout
    if data == (b'f_stop'):
        print(data)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(0)
    #前出すぎたらストップ
    if data == (b'Stop'):
        print(data)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(0)

    #tar_x1 < 250
    if data == (b'turn_left1'):
        print(data)
        mv_angle(-30)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED) 
    #tar_x1 < 500
    if data == (b'turn_left2'):
        print(data)
        mv_angle(-20)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED) 
    #tar_x1 < 375
    # if data == (b'turn_left3'):
    #     print(data)
    #     mv_angle(2)
    #     GPIO.output(sets.DIR, GPIO.HIGH)
    #     p1.start(sets.turn_SPEED) 

    #tar_x1 > 500
    if data == (b'turn_right1'):
        print(data)
        mv_angle(30)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED)
    #375 < tar_x1 <= 500
    if data == (b'turn_right2'):
        print(data)
        mv_angle(20)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED)
    # if data == (b'turn_right3'):
    #     print(data)
    #     mv_angle(-2)
    #     GPIO.output(sets.DIR, GPIO.HIGH)
    #     p1.start(sets.turn_SPEED)

    if data == 0:
        mv_angle(0)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(0)
        break

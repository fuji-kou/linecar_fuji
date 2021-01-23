import socket
from time import sleep
import sys
import os
<<<<<<< HEAD
#import RPi.GPIO as GPIO
=======
import RPi.GPIO as GPIO
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
# sys.path.append('..')
import linecar_settings as sets

# pin設定
<<<<<<< HEAD
# GPIO.setmode(GPIO.BCM)      
# GPIO.setwarnings(False)             #GPIOからの警告を有効にする

# GPIO.setup(sets.pwm, GPIO.OUT)      #出力設定          
# GPIO.setup(sets.DIR, GPIO.OUT)
# GPIO.setup(sets.Servo_pin, GPIO.OUT)  
# sleep(1)

# p1 = GPIO.PWM(sets.pwm, 100)            #pwmピンの設定
# Servo = GPIO.PWM(sets.Servo_pin, 50) 
# Servo.start(0)                      

# servo
# def mv_angle(angle):
#     duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
#     Servo.ChangeDutyCycle(duty)     #デューティ比を変更
=======
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
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバを指定
#同端末
<<<<<<< HEAD
sock.connect(('127.0.0.1', 50008))
#ファーウェイタブ（ラズパイとの通信）DELL
#sock.connect(('192.168.43.198', 50006))
=======
#sock.connect(('127.0.0.1', 50009))
#ファーウェイタブ（ラズパイとの通信）DELL
sock.connect(('192.168.43.198', 50006))
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
#宮本研DELL 
#sock.connect(('192.168.11.12', 50006))


#sock.connect(('192.168.179.4', 50006))
#実機HP_PC
<<<<<<< HEAD
#sock.connect(('192.168.179.2', 50008))#ポケットwihi
=======
#sock.connect(('192.168.179.2', 54202))#ポケットwihi
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
#sock.connect(('192.168.11.34',50008))#恐らく宮本研wihi

#sock.connect(('192.168.11.12',50008))

# サーバにメッセージを送る
while True:
    sock.sendall(b'connect')

        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = sock.recv(1024)

    #開始・floutからの復帰  
    if data == (b'start!!'):
        print(data)
        sleep(2)
<<<<<<< HEAD
        # mv_angle(0)
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(sets.SPEED)
=======
        mv_angle(0)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.SPEED)
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
        
    #離れすぎたら前に出る
    if data == (b'Go1'):
        print(data)
<<<<<<< HEAD
        # mv_angle(0)
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(sets.SPEED)
=======
        mv_angle(0)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.SPEED)
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
    if data == (b'Go2'):
        pass
    #flout
    if data == (b'stop!!'):
        print(data)
<<<<<<< HEAD
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(0)
    #前出すぎたらストップ
    if data == (b'Stop1'):
        print(data)
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(0)
=======
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(0)
    #前出すぎたらストップ
    if data == (b'Stop1'):
        print(data)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(0)
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
    if data == (b'Stop2'):
        pass
    #範囲から出たとき
    if data == (b'turn_left1'):
        print(data)
<<<<<<< HEAD
        # mv_angle(-20)
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(sets.turn_SPEED) 
=======
        mv_angle(20)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED) 
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
    if data == (b'turn_left2'):
        pass
    #範囲から出たとき
    if data == (b'turn_right1'):
        print(data)
<<<<<<< HEAD
        # mv_angle(20)
        # GPIO.output(sets.DIR, GPIO.HIGH)
        # p1.start(sets.turn_SPEED)
    if data == (b'turn_right2'):
        pass

    if data == 0:
        #mv_angle(0)
=======
        mv_angle(-20)
        GPIO.output(sets.DIR, GPIO.HIGH)
        p1.start(sets.turn_SPEED)
    if data == (b'turn_right2'):
        pass

    # if data == (b'turn_left1!'):
    #     print(data)
    #     mv_angle(20)
    #     GPIO.output(sets.DIR, GPIO.HIGH)
    #     p1.start(sets.turn_SPEED) 
    # if data == (b'turn_left2!'):
    #     pass
    # #範囲から出たとき
    # if data == (b'turn_right1!'):
    #     print(data)
    #     mv_angle(-20)
    #     GPIO.output(sets.DIR, GPIO.HIGH)
    #     p1.start(sets.turn_SPEED)
    # if data == (b'turn_right2!'):
    #     pass



    if data == 0:
        mv_angle(0)
>>>>>>> fcf57261f394e97c09bf3e6c2fe22428f069de3d
        break
















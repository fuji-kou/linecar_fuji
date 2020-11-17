import sys
import time
import pygame
from pygame.locals import *
#import pigpio
import RPi.GPIO as GPIO     
from time import sleep
#from servo_motor import angle


GPIO.setmode(GPIO.BCM)      
GPIO.setwarnings(False)             #GPIOからの警告を有効にする

Servo_pin = 18
GPIO.setup(Servo_pin, GPIO.OUT)  
sleep(1)

Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])
Servo.start(0)                      #Servo.start(デューティ比[0-100%])
def servo_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)     #デューティ比を変更
    time.sleep(0.3)                 

def main():  
    #パイゲームとジョイスティックの初期化
         
    pygame.init()
    
    try:
    
        
        print(joystick.get_name())
    except pygame.error:
        print('ジョイスティックが接続されていません．')
        
    print('Ready!')
    
    
    l_stick = 0.0
    active = True
    while active:
        servo_angle(0)
        input_angle = -130*l_stick
        if round(input_angle) > 30:
            servo_angle(30)
        if round(input_angle) < -30:
            servo_angle(-30)
        servo_angle(round(input_angle, 1))
     
        

        for e in pygame.event.get():      #イベントチェック
            if e.type == pygame.locals.JOYAXISMOTION:
                if e.axis == 1:
                    l_stick = joystick.get_axis(0)              #Joystick.get_axis:操作レバーの現在の傾き位置を取得 0:レバーは中央  get_axis:軸番号：(0):左右、(1)：上下


           
    

if __name__ == '__main__':
    pygame.joystick.init()
    try:
        joystick = pygame.joystick.Joystick(0)      #joystick instanceの作成
        joystick.init()                             #init instance
        main()
    except KeyboardInterrupt:          
        servo_angle(0)
        Servo.stop()                   #サーボモータをストップ
        GPIO.cleanup()                 #GPIOをクリーンアップ
        sys.exit()                     #プログラムを終了
        
  

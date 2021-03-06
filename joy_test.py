import time
import sys
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO     
from time import sleep
from models import LineCar

m1 = LineCar.LineCar()
def main():  
    #パイゲームとジョイスティックの初期化
    pygame.joystick.init()      
    pygame.init()
    
    try:
        joystick = pygame.joystick.Joystick(0)      #joystick instanceの作成
        joystick.init()                             #init instance
        print(joystick.get_name())
    except pygame.error:
        print('ジョイスティックが接続されていません．')
        
    print('Ready!')
    
    l2trigger = 0.0
    l_stick = 0.0
    x_button = False
    o_button = False
    active = True
     
    while active:
        
        if l2trigger > 0.2:
            input_speed = 10
        else:
            input_speed = 0
                

        for e in pygame.event.get():      #イベントチェック
            if e.type == pygame.locals.JOYAXISMOTION:
                if e.axis == 1:
                    l_stick = joystick.get_axis(0)#Joystick.get_axis:操作レバーの現在の傾き位置を取得 0:レバーは中央
                    input_angle = -130*l_stick
                    if round(input_angle) >= 30:
                        m1.mv_angle(30)
                    if round(input_angle) <= -30:
                        m1.mv_angle(-30)
                    if round(input_angle) == 0:
                        m1.mv_angle(0)
                    
                if e.axis == 5:
                    l2trigger = joystick.get_axis(5)
                    GPIO.output(m1.DIR, GPIO.HIGH)
                    m1.p1.start(input_speed)         #速度設定0－100
                    if input_speed >= 5:
                        m1.p1.start(5)
                        
            elif e.type == pygame.locals.JOYBUTTONDOWN:        #ボタン押す
                if e.button == 10:                             #e.botton:ボタン番号
                    active = False
                    break
                if e.button == 0:
                    GPIO.output(m1.DIR, GPIO.LOW)        
                    input_speed = -1*input_speed
                     
            elif e.type == pygame.locals.JOYBUTTONUP: #ボタン離れる
                if e.button == 0:
                    x_button = False

if __name__ == '__main__':
    pygame.joystick.init()
    try:
        joystick = pygame.joystick.Joystick(0)      #joystick instanceの作成
        joystick.init()                             #init instance
        main()
    except KeyboardInterrupt:          
        #m1.mv_angle(0)
        m1.mv_angle(0)
        Servo.stop()                   #サーボモータをストップ         p1.start(0)
        GPIO.cleanup()                 #GPIOをクリーンアップ
        sys.exit()                     #プログラムを終了

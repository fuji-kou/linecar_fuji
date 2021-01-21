# coding: utf-8
import numpy as np
import csv
import sys
import RPi.GPIO as GPIO
import time
from time import sleep

import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl

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

mv_angle(0)
p1.start(40)
    
def main():
    record = []

    m1 = LineCar()
    m1.setup4experiment()
    mv_angle(0)
    m1.controller.prepare()
    # 発進
    GPIO.output(sets.DIR, GPIO.HIGH)  
    p1.start(20)
    # 操作ループ
    while(True):
        try:
            now_latlon = m1.get_current_position()
            input_angle = m1.controller.get_input_angle(now_latlon)
            #mv_angle(round(input_angle, 1))
            record.append(m1.get_status())
            print(record[-1])
            if m1.controller.is_finished():
                 p1.start(10)
                 break
        except KeyboardInterrupt:
            m1.stop()
            p1.start(10)

    #終了処理
    m1.stop()
    p1.start(0)

    with open('output.csv', 'w') as csv_out:
        writer = csv.writer(csv_out, lineterminator='\n')
        writer.writerows(record)


if __name__ == '__main__':
    main()
import RPi.GPIO as GPIO             
import time                         #
import sys                          


Servo_pin = 18                      

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Servo_pin, GPIO.OUT)     

#PWMの設定
Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])
Servo.start(0)                      #Servo.start(デューティ比[0-100%])

#角度からデューティ比を求める関数
def servo_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)     #デューティ比を変更
    time.sleep(0.3)



#動作テスト：サーボモータの角度をデューティ比で制御(デューティ比[0-100%])
"""
while True:
    try:
        servo_angle(0)
        time.sleep(1)
        servo_angle(-30)               #サーボモータ -30°
        time.sleep(1)
        servo_angle(0)
        time.sleep(1)
        servo_angle(30)                #サーボモータ  30°
        time.sleep(1)

    except KeyboardInterrupt:          #Ctrl+Cキーが押された
        servo_angle(0)
        Servo.stop()                   #サーボモータをストップ
        GPIO.cleanup()                 #GPIOをクリーンアップ
        sys.exit()                     #プログラムを終了
"""
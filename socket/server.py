import socket
import time
import RPi.GPIO as GPIO


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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #ソケット作成
    # IPアドレスとポートを指定
    s.bind(('127.0.0.1', 50007))
    #s.bind(('255.255.255.0', 50007))
    #s.bind(('192.168.43.198', 50007))
    #  接続(最大2)
    s.listen(2)
    # connection するまで待つ
    while True:
        # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
        conn, addr = s.accept()
        with conn:
            while True:
                # データを受け取る
                data = conn.recv(1024)
                p1.start(10)
                if not data:
                    break
                print('data : {}, addr: {}'.format(data, addr))
                # クライアントにデータを返す(b -> byte でないといけない)
                conn.sendall(b'Received: ' + data)



    # except KeyboardInterrupt:
    #     print('!!FINISH!!')
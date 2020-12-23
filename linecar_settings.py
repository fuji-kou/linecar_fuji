# # serial
# #COM_PORT = '/dev/ttyACM0'
# COM_PORT = "/dev/input/js0"
# BAUDRATE = '38400'
# TIMEOUT = 0.1

# raspi(pin)
Servo_pin = 18
pwm = 23                           #pwmピンを23に設定
DIR = 24                           #DIRピンを24に設定

# socket
ADDRESS = '127.0.0.1'
PORT_NUM = 52002
BUFSIZE = 256

#FujitaControl
GAIN_FJT = 5
SPEED = 15
REFERENCE_POINT = [33.8896798200639, 130.709442745616]
POSITION_END = [33.8896655366181, 130.709388048545]
POSITION_START = [33.8896798200639, 130.709442745616]

# # FixedAngleTest
# INPUT_ANGLE = 530.0
# INPUT_TIME = 10
# ENDING_TIME = 30
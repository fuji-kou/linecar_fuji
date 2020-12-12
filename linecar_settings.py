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
SPEED = 10
REFERENCE_POINT = [33.8896054, 130.709148]
POSITION_END = [33.889629411, 130.709264713]
POSITION_START = [33.889575738, 130.709056720]

# # FixedAngleTest
# INPUT_ANGLE = 530.0
# INPUT_TIME = 10
# ENDING_TIME = 30
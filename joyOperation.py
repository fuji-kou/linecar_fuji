import serial
import time
import pygame
from pygame.locals import *

from models.LineCar import LineCar


def main():
    pygame.joystick.init()
    pygame.init()
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(joystick.get_name())
    except pygame.error:
        print('ジョイスティックが接続されていません．')


    m1 = LineCar()
    m1.setup4movement()
    print('Ready!')

    l2trigger = 0.0
    l_stick = 0.0
    x_button = False
    active = True
    while active:

        for e in pygame.event.get():
            if e.type == pygame.locals.JOYAXISMOTION:
                if e.axis == 0:
                    l_stick = joystick.get_axis(0)       
                if e.axis == 5:
                    l2trigger = joystick.get_axis(5)
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                if e.button == 12:
                    active = False
                    break
                if e.button == 2:
                    x_button = True               
            elif e.type == pygame.locals.JOYBUTTONUP:
                if e.button == 2:
                    x_button = False

        input_angle = -750*l_stick
        input_speed = 0 if (l2trigger>0.9) else 50*(1-(l2trigger+1)/2)
        if x_button:
            input_speed = -1*input_speed
        
        m1.mv_wheel(round(input_speed, 1))
        m1.mv_angle(round(input_angle, 1))
        time.sleep(0.005)
    

    m1.stop()


if __name__ == '__main__':
    main()

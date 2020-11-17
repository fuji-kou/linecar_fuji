import pigpio
import time
 
gpio_pin0 = 18
 
pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)


pi.hardware_PWM(gpio_pin0,50,10000)
 
time.sleep(2)
# GPIO18: 50Hz、duty比2.5%
pi.hardware_PWM(gpio_pin0,50,25000)
 
time.sleep(2)
 
# GPIO18: 50Hz、duty比7.25%
pi.hardware_PWM(gpio_pin0,50,72500)
 
time.sleep(2)
 
# GPIO18: 50Hz、duty比12%
pi.hardware_PWM(gpio_pin0,50,120000)
 
time.sleep(2)
 
pi.set_mode(gpio_pin0,pigpio.INPUT)
pi.stop()
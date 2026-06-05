#tbi

from machine import Pin
import time

trigger = Pin(5, Pin.OUT)
echo = Pin(4, Pin.IN)

def get_distance ():
    trigger.value(0)
    time.sleep_us(10)

    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    timeout_i = time.ticks_us()
    while echo.value() == 0:
        if (time.ticks_diff(time.ticks_us(), timeout_i) > 23200):
            return -1
    
    if echo.value():
        ti = time.ticks_us()

        while echo.value() == 1:
            if (time.ticks_diff(time.ticks_us(), ti) > 23200):
                return -1 # > 4m
        
        delta_t = time.ticks_diff(time.ticks_us(), ti)
        # 343 m/s = 34300 cm / s = 34300 cm / 10^6 us = 0.0343 cm/us
        distance = delta_t * 0.0343 / 2

        return distance
    else:
        return -2 # not enough precision
    
while True:
    delta_x = get_distance()
    if (delta_x == -2):
        print("Not enough precision.")
    elif (delta_x == -1):
        print("Too far to detect.")
    else:
        print("Distance: {delta_x:.2f} cm.")

    time.sleep(0.5)

#tbi
from machine import Pin, PWM
import time

servo_pin = Pin(14, Pin.OUT)
servo = PWM(servo_pin, freq=50)

def move_servo(angle):
    if 0 <= angle <= 180:
        duty = int(26 + (angle / 180) * (123 - 26))
        servo.duty(duty)
    else:
        print("Angle out of range (0-180)")

print("Servo on.")

for i in range(3):
    print("Moving to 0 degrees.")
    move_servo(0)
    time.sleep(3)

    print("Moving to 90 degrees.")
    move_servo(90)
    time.sleep(3)

    print("Moving to 180 degrees.")
    move_servo(180)
    time.sleep(3)

servo.deinit()
print("Servo off.")
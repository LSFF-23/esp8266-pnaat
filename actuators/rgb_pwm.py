#tbi
from machine import Pin, PWM
import time

pwm_red = PWM(Pin(14, Pin.OUT))
pwm_green = PWM(Pin(12, Pin.OUT))
pwm_blue = PWM(Pin(13, Pin.OUT))

colors = [
    (100, 0, 0),
    (0, 100, 0),
    (0, 0, 100),
    (100, 100, 0),
    (0, 100, 100),
    (100, 0, 100),
    (100, 100, 100),
    (100, 50, 0),
]

def set_color(r_pct, g_pct, b_pct):
    pwm_red.duty(r_pct // 100 * 1024)
    pwm_green.duty(g_pct // 100 * 1024)
    pwm_blue.duty(b_pct // 100 * 1024)

while True:
    for r, g, b in colors:
        print(f"Setting color to: R={r}% G={g}% B={b}%")
        set_color(r, g, b)
        time.sleep(2)
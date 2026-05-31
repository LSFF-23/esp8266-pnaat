from machine import Timer, Pin, ADC, PWM
import time

led = Pin(2, Pin.OUT)
led_pwm = PWM(led, freq=1000)
led_timer = Timer(-1)
a0 = ADC(0)
a0_raw = a0.read()

def t_callback (t):
    led_pwm.duty(a0_raw)
    print(f"Novo estado do led: {a0_raw}")

led_timer.init(period=500, mode=Timer.PERIODIC, callback=t_callback)

print ("Timer iniciado")

while True:
    a0_raw = a0.read()
    time.sleep(1)
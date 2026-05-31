from machine import Pin
import time

ti = time.ticks_ms()

led = Pin(2, Pin.OUT)
d5 = Pin(14, Pin.IN, Pin.PULL_UP)

d5_pressed = False
def d5_keydown (event_pin):
    global d5_pressed
    print(f"[{time.ticks_diff(time.ticks_ms(), ti):08d}] O botão {event_pin} foi pressionado!")
    d5_pressed = True

d5.irq(trigger=Pin.IRQ_FALLING, handler=d5_keydown)

loop_counter = 0
print("Loop iniciado...")
while True:
    time.sleep(1)

    if (d5_pressed):
        d5_pressed = False
        led.toggle()
        print(f"[{time.ticks_diff(time.ticks_ms(), ti):08d} Alterando o valor do led, agora ele é: {led.value()}")

    loop_counter += 1
    print(f"[{time.ticks_diff(time.ticks_ms(), ti):08d}] Fim do loop. Iteração: {loop_counter}")

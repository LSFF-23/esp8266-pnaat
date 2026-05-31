from machine import Pin
import time

D0 = Pin(16, Pin.IN)
led = Pin(2, Pin.OUT)

print("Starting...")

reg_sync1 = 0
reg_sync2 = 0
led.value(0)

while True:
    reg_sync2 = reg_sync1
    reg_sync1 = D0.value()
    
    if reg_sync2 == 0 and reg_sync1 == 1:
        led.toggle()
        print(f"Button pushed! Led state: {'Off' if led.value() else 'On'}.")
    
    time.sleep(0.05)
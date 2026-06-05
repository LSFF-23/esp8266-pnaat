from machine import Pin, ADC
import time

# max for esp8266 = 1024
a0 = ADC(0)
d5 = Pin(14, Pin.OUT)
d6 = Pin(12, Pin.OUT)
d7 = Pin(13, Pin.OUT)

print("Starting...")

def a0_get (sample_size = 20, time_window = 400):
    delay_value = time_window // sample_size
    mean = 0
    for _ in range(sample_size):
        mean += a0.read()
        time.sleep_ms(delay_value)
    return mean // sample_size

while True:
    a0_raw = a0_get()
    
    print(f"Raw Mean: {a0_raw}")
    if (a0_raw >= 0 and a0_raw < 256):
        d5.value(0)
        d6.value(0)
        d7.value(0)
    elif (a0_raw >= 256 and a0_raw < 512):
        d5.value(0)
        d6.value(0)
        d7.value(1)
    elif (a0_raw >= 512 and a0_raw < 768):
        d5.value(0)
        d6.value(1)
        d7.value(1)
    else:
        d5.value(1)
        d6.value(1)
        d7.value(1)
    
    time.sleep_ms(600)

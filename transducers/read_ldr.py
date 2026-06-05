from machine import Pin, ADC
import time

a0 = ADC(0)

def a0_get (sample_size = 20, time_window = 400):
    delay_value = time_window // sample_size
    mean = 0
    for _ in range(sample_size):
        mean += a0.read()
        time.sleep_ms(delay_value)
    return mean // sample_size

while True:
    a0_raw = a0.get()
    raw_percent = (a0_raw / 1024) * 100
    print(f"Raw: {a0_raw} | Luminosidade: {raw_percent:02.1f}%")
    time.sleep_ms(600)
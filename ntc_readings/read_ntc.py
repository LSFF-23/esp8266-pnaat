from machine import Pin, ADC
import time, math

a0 = ADC(0)
led = Pin(2, Pin.OUT)

def a0_get (sample_size = 20, time_window = 400):
    delay_value = time_window // sample_size
    mean = 0
    for _ in range(sample_size):
        mean += a0.read()
        time.sleep_ms(delay_value)
    return mean // sample_size

def get_temp (raw, max_raw = 1024):
    R_VD = 10_000
    R0_NTC = 10_000
    C0_NTC = 25
    T0_NTC = C0_NTC + 273.15
    BETA = 3950
    
    r_ntc = R_VD * ((max_raw / raw) - 1)
    t_kelvin = 1 / ((1 / T0_NTC) + (1.0 / BETA) * math.log(r_ntc / R0_NTC));
    return t_kelvin - 273.15

while True:
    a0_raw = a0_get()
    led.value(1)
    
    if a0_raw > 0 and a0_raw < 1024:
        temperature = get_temp(a0_raw)
        print(f"Raw: {a0_raw:04d} | Temperature: {temperature:02.1f}")
        if (temperature >= 37): # body temperature
            led.value(0)
    else:
        print(f"Invalid reading this time: {a0_raw:04d}. Skipping...")
    
    time.sleep_ms(600)

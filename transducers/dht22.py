#tbi

from machine import Pin
import time
import dht

sensor = dht.DHT22(Pin(15))

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity() 
        print(f"Temperature: {temperature}°C | Humidity: {humidity}%")
    except OSError as e:
        print("Error: ", e)
    
    time.sleep(2)
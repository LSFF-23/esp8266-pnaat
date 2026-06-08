from machine import Pin, ADC
from umqtt.simple import MQTTClient
import time
import network
import math
import config

CLIENT_ID = "esp8266_node42"
TOPIC_TEMP = b"esp8266/ntc/temperature"
TOPIC_RELAY = b"esp8266/relay/command"

analog_pin = ADC(0)
relay_led = Pin(2, Pin.OUT, value=1)

def connect_wifi ():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
        while not wlan.isconnected():
            time.sleep_ms(500)
    print("WiFi Connected! IP:", wlan.ifconfig()[0])

def get_temp (raw, max_raw = 1024):
    if raw == 0:
        return -273.15
    if raw == max_raw:
        return 100
    
    R_VD = 10_000
    R0_NTC = 10_000
    C0_NTC = 25
    T0_NTC = C0_NTC + 273.15
    BETA = 3950
    
    r_ntc = R_VD * ((max_raw / raw) - 1)
    t_kelvin = 1 / ((1 / T0_NTC) + (1.0 / BETA) * math.log(r_ntc / R0_NTC));
    return t_kelvin - 273.15

def command_callback (topic, msg):
    msg = msg.strip().lower()
    print(f"MQTT Message[{topic.decode()}]: {msg.decode()}")
    if msg in b"1onligar":
        relay_led.value(0)
        print("Relay Enabled!")
    elif msg in b"0offdesligar":
        relay_led.value(1)
        print("Relay Disabled!")

connect_wifi()

client = MQTTClient(CLIENT_ID, config.MQTT_BROKER)
client.set_callback(command_callback)
client.connect()
print(f"Connected to MQTT Broker: {config.MQTT_BROKER}")

client.subscribe(TOPIC_RELAY)
print(f"Subscribed to: {TOPIC_RELAY.decode()}")

last_send = 0

try:
    while True:
        client.check_msg()
        now = time.time()
        if now - last_send >= 5:
            temp = get_temp(analog_pin.read())
            payload = f"{temp:.2f}"
            print(f"Publishing Temperature: {payload} °C")
            client.publish(TOPIC_TEMP, payload.encode())
            last_send = now
        time.sleep_ms(100)

except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
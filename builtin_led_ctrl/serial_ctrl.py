from machine import Pin
import time

led = Pin(2, Pin.OUT)

print("Iniciando...")
while True:
    print("Insira um comando")
    command = input().strip().lower()

    if command in '1onligar':
        led.value(0)
        print("O led foi ligado!")
    elif command in '0offdesligar':
        led.value(1)
        print("O led foi desligado!")
    else:
        print("Comando inválido!")
    
    time.sleep_ms(200)
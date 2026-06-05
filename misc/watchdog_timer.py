#tbi
from machine import WDT
import time
wdt = WDT(timeout=5000)

print("Timeout = 5s")

print("Iniciando...")
for i in range(15):
    print(f"Ciclo {i+1}/15")
    wdt.feed()
    time.sleep(1)

print("Deadlock")
while True:
    pass
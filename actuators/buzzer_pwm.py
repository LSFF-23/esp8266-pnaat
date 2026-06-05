#tbi
from machine import Pin, PWM
import time

buzzer_pin = Pin(14, Pin.OUT)
buzzer = PWM(buzzer_pin)

NOTE_F4 = 349
NOTE_A4 = 440
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_E5 = 659
NOTE_D5 = 587
NOTE_G4 = 392
NOTE_E4 = 330
NOTE_D4 = 293

melody = [
    (NOTE_F4, 8), (NOTE_A4, 8), (NOTE_B4, 4),
    (NOTE_F4, 8), (NOTE_A4, 8), (NOTE_B4, 4),
    (NOTE_F4, 8), (NOTE_A4, 8), (NOTE_B4, 8), (NOTE_E5, 8), (NOTE_D5, 4),
    (NOTE_B4, 8), (NOTE_C5, 8), (NOTE_B4, 8), (NOTE_G4, 8), (NOTE_E4, 2),
    (NOTE_D4, 8), (NOTE_E4, 8), (NOTE_F4, 8), (NOTE_G4, 8), (NOTE_A4, 2),
    (NOTE_B4, 4), (NOTE_C5, 4), (NOTE_B4, 2),
]

BPM = 140
BEAT_DURATION_MS = int(60000 / BPM)

def play_note(frequency, note_type):
    if frequency == 0:
        buzzer.duty(0)
    else:
        duration = int(BEAT_DURATION_MS * (4 / note_type))
        buzzer.freq(frequency)
        buzzer.duty(512)
        time.sleep_ms(duration)
        buzzer.duty(0)
        time.sleep_ms(int(duration * 0.1))

print("Playing \"Lost Woods\"")

for i in range(3):
    for note, note_type in melody:
        play_note(note, note_type)
    time.sleep(2)

buzzer.duty(0)
print("Song finished.")
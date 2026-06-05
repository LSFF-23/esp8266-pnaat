uint8_t d5 = 14;
uint8_t d6 = 12;
uint8_t d7 = 13;

void setup() {
  Serial.begin(115200);
  pinMode(d5, OUTPUT);
  pinMode(d6, OUTPUT);
  pinMode(d7, OUTPUT);
}

int get_a0 () {
    int mean = 0;
    for (int i = 0; i < 20; i++) {
      mean += analogRead(A0);
      delay(20);
    }
    return mean / 20;
}


void loop() {
  int a0_raw = get_a0();
  Serial.print("Raw Mean: ");
  Serial.println(a0_raw);

  if (a0_raw >= 0 && a0_raw < 256) {
    digitalWrite(d5, 0);
    digitalWrite(d6, 0);
    digitalWrite(d7, 0);
  } else if (a0_raw >= 256 && a0_raw < 512) {
    digitalWrite(d5, 0);
    digitalWrite(d6, 0);
    digitalWrite(d7, 1);
  } else if (a0_raw >= 512 && a0_raw < 768) {
    digitalWrite(d5, 0);
    digitalWrite(d6, 1);
    digitalWrite(d7, 1);
  } else {
    digitalWrite(d5, 1);
    digitalWrite(d6, 1);
    digitalWrite(d7, 1);
  }

  delay(600);
}
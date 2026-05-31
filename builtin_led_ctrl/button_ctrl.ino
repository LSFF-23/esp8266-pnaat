bool reg_sync1 = 0;
bool reg_sync2 = 0;
bool led_state = 0;
uint8_t D0 = 16;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D0, INPUT);

  digitalWrite(LED_BUILTIN, LOW);
}


void loop() {
  reg_sync2 = reg_sync1;
  reg_sync1 = digitalRead(D0);

  if (!reg_sync2 && reg_sync1) {
    led_state = !digitalRead(LED_BUILTIN);
    digitalWrite(LED_BUILTIN, led_state);
    Serial.print("Button pushed! Led state: ");
      if (led_state)
        Serial.print("Off.\n");
      else
        Serial.print("On.\n");
  }

  delay(50);
}
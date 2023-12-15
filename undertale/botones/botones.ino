const int btnLeft = 2;
const int btnRight = 3;
const int btnUp = 4;
const int btnDown = 5;

void setup() {
  Serial.begin(9600);
  pinMode(btnLeft, INPUT);
  pinMode(btnRight, INPUT);
  pinMode(btnUp, INPUT);
  pinMode(btnDown, INPUT);
}

void loop() {
  if (digitalRead(btnLeft) == HIGH) {
    Serial.write('L');
  }
  if (digitalRead(btnRight) == HIGH) {
    Serial.write('R');
  }
  if (digitalRead(btnUp) == HIGH) {
    Serial.write('U');
  }
  if (digitalRead(btnDown) == HIGH) {
    Serial.write('D');
  }
  delay(50);
}

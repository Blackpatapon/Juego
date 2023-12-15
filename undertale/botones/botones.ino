const int btnLeft = 2;
const int btnRight = 3;
const int btnUp = 4;
const int btnDown = 5;
const int btnEnter = 6; // Agregamos un quinto pulsador

void setup() {
  Serial.begin(9600);
  pinMode(btnLeft, INPUT);
  pinMode(btnRight, INPUT);
  pinMode(btnUp, INPUT);
  pinMode(btnDown, INPUT);
  pinMode(btnEnter, INPUT); // Configuramos el nuevo pulsador
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
  if (digitalRead(btnEnter) == HIGH) {
    Serial.write('E'); // Puedes usar cualquier letra o símbolo para representar la tecla "Enter"
  }
  delay(50);
}

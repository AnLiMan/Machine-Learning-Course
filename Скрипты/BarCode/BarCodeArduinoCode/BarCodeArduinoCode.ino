#define Action1 9 //Пин на первое действие
#define Action2 10 //Пин на второе действие
#define Action3 11 //Пин на третье действие
int data; //Переменная для хранения получаемого символа

void setup() {
  Serial.begin(19200); //Запускаем последовательный порт, скорость 19200 бод
  //Конфигурим пины
  pinMode(Action1, OUTPUT);
  pinMode(Action2, OUTPUT);
  pinMode(Action3, OUTPUT);

  Serial.setTimeout(1);

  digitalWrite(Action1, LOW);
  digitalWrite(Action2, LOW);
  digitalWrite(Action3, LOW);
}

void loop() {
  while (!Serial.available());
  data = Serial.readString().toInt();
  Serial.print(data);
  
  //Если приняли ноль
  if (data == 0) {
    digitalWrite(Action1, HIGH);
    digitalWrite(Action2, LOW);
    digitalWrite(Action3, LOW);
  }
  //Если приняли 1
  else if (data == 1) {
    digitalWrite(Action1, LOW);
    digitalWrite(Action2, HIGH);
    digitalWrite(Action3, LOW);
  }
   //Если приняли 2
  else if (data == 2) {
    digitalWrite(Action1, LOW);
    digitalWrite(Action2, LOW);
    digitalWrite(Action3, HIGH);
  }
}

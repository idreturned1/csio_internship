void setup() {

  Serial.begin(9600);

}

void loop() {

  int i = 1, s1, s2, s3, s4, s5;

  while (i > 0) {


    s1 = analogRead(A0);
    s2 = analogRead(A1);
    s3 = analogRead(A2);
    s4 = analogRead(A3);
    s5 = analogRead(A4);
    Serial.print(s1);
    Serial.print(',');
    Serial.print(s2);
    Serial.print(',');
    Serial.print(s3);
    Serial.print(',');
    Serial.print(s4);
    Serial.print(',');
    Serial.println(s5);

    i++;
    delay(1000);
  }




}


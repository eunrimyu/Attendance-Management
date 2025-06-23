
int sensor0 = A0;                           // 센서값을 아나로그 A0핀 설정
int sensor1 = A1;                           // 센서값을 아나로그 A0핀 설정
int sensor2 = A2;                           // 센서값을 아나로그 A0핀 설정
int sensor3 = A3;                           // 센서값을 아나로그 A0핀 설정

int value = 0;                                       // loop에서 사용할 변수 설정



void setup()

{ 

  Serial.begin(9600);                   

}



void loop()

{

  int value0 = analogRead(sensor0);
  int value1 = analogRead(sensor1);
  int value2 = analogRead(sensor2);
  int value3 = analogRead(sensor3);
  
  //Serial.print("0, ");
  Serial.println(value0);
  /*Serial.print("1, ");
  Serial.println(value1);
  Serial.print("2, ");
  Serial.println(value2);
  Serial.print("3, ");
  Serial.println(value3);
*/

  delay(3000);                               

}

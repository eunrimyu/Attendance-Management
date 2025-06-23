int sensor0 = A0;
int sensor1 = A1;
int sensor2 = A2;
int sensor3 = A3;
int point = 4;
bool previous0State = false;
bool previous1State = false;
bool previous2State = false;
bool previous3State = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value0 = analogRead(sensor0);
  int value1 = analogRead(sensor1);
  int value2 = analogRead(sensor2);
  int value3 = analogRead(sensor3);

  bool current0State = (value0 > point);
  bool current1State = (value1 > point);
  bool current2State = (value2 > point);
  bool current3State = (value3 > point);
  
  if (current0State != previous0State) {
    if (current0State) {
      Serial.println("sensor_0 sit");
    } else {
      Serial.println("sensor_0 stand");
    }
  }
  if (current1State != previous1State) {
    if (current1State) {
      Serial.println("sensor_1 sit");
    } else {
      Serial.println("sensor_1 stand");
    }
  }
  if (current2State != previous2State) {
    if (current2State) {
      Serial.println("sensor_2 sit");
    } else {
      Serial.println("sensor_2 stand");
    }
  }
  if (current3State != previous3State) {
    if (current3State) {
      Serial.println("sensor_3 sit");
    } else {
      Serial.println("sensor_3 stand");
    }
  }
  previous0State = current0State;
  previous1State = current1State;
  previous2State = current2State;
  previous3State = current3State;
  delay(1000);
}

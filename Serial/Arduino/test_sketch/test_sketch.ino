#define MR_F 6
#define ML_F 5
#define ML_B 9
#define MR_B 10


void forward(){
  analogWrite(MR_F, 255);
  analogWrite(MR_B, 0);
  analogWrite(ML_F, 255);
  analogWrite(ML_B, 0);
}


void backward(){
  analogWrite(MR_F, 0);
  analogWrite(MR_B, 255);
  analogWrite(ML_F, 0);
  analogWrite(ML_B, 255);
}

void quick_turnR(){
  analogWrite(MR_F, 0);
  analogWrite(MR_B, 255);
  analogWrite(ML_F, 255);
  analogWrite(ML_B, 0);
}

void quick_turnL(){
  analogWrite(MR_F, 255);
  analogWrite(MR_B, 0);
  analogWrite(ML_F, 0);
  analogWrite(ML_B, 255);
}


void stopCar(){
  analogWrite(MR_F, 0);
  analogWrite(MR_B, 0);
  analogWrite(ML_F, 0);
  analogWrite(ML_B, 0);
}

void setup() {
  pinMode(MR_F,OUTPUT);
  pinMode(MR_B,OUTPUT);
  pinMode(ML_F,OUTPUT);
  pinMode(ML_B,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    char val = Serial.read();
    Serial.write(val);
    if(val == 'F'){
      forward();
    }
    if(val == 'B'){
      backward();
    }
    if(val == 'S'){
      stopCar();
    }
    if(val == 'L'){
      quick_turnL();
    }
    if(val == 'R'){
      quick_turnR();
    }
  }
}

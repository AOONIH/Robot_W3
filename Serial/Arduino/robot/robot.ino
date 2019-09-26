#define MR_F 6
#define ML_F 5
#define ML_B 9
#define MR_B 10

#define EchoPinL 3
#define TrigPinL 2

#define EchoPinR A6
#define TrigPinR A7

#define crit 100 // value above background
#define max_thresh 500 // value above background for stop
#define range max_thresh-crit
#define D_close_threshold 10
#define light_turn_threhsold 100
#define len_ldr 10


int stop_or_driveL = 0;
int stop_or_driveR = 0;
int sample_lum     = 1;
unsigned long explore_travel_until = 0;
int explore_state  = 1;
int init_flg = 0;
char explore_movement = 'F';
unsigned long sweep_until = 0;
unsigned long time_LED_toggled = 0;

int background;

int L_ldr_arr[len_ldr];
int R_ldr_arr[len_ldr];


unsigned long distanceL(){
  digitalWrite(TrigPinL, LOW);
  delayMicroseconds(2);
  digitalWrite(TrigPinL, HIGH);
  delayMicroseconds(10);
  digitalWrite(TrigPinL, LOW);
  unsigned long duration = pulseIn(EchoPinL, HIGH);
  return duration * 0.034 / 2;
}

unsigned long distanceR(){
  digitalWrite(TrigPinR, LOW);
  delayMicroseconds(2);
  digitalWrite(TrigPinR, HIGH);
  delayMicroseconds(10);
  digitalWrite(TrigPinR, LOW);
  unsigned long duration = pulseIn(EchoPinR, HIGH);
  return duration * 0.034 / 2;
}


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

void quick_turnR(int speed = 255){
  analogWrite(MR_F, 0);
  analogWrite(MR_B, speed);
  analogWrite(ML_F, speed);
  analogWrite(ML_B, 0);
}

void quick_turnL(int speed = 255){
  analogWrite(MR_F, speed);
  analogWrite(MR_B, 0);
  analogWrite(ML_F, 0);
  analogWrite(ML_B, speed);
}


void avoid(bool left_approach, bool right_approach){
  if(left_approach and !right_approach){
    quick_turnR();
    if(explore_movement == 'L') explore_movement = 'R';
    delay(1000);
  }else if(!left_approach and right_approach){
    quick_turnL();
    if(explore_movement == 'R') explore_movement = 'L';
    delay(1000);
  }else if(left_approach and right_approach){    
    backward();
    delay(700);
    quick_turnR();
    delay(200);
  }
}

void explore(unsigned long time){
  if(time > explore_travel_until){
    if(explore_movement == 'F'){
      explore_travel_until = time + 300*random(1, 10);
      int tmp = random(0,2);
      if(tmp == 0){
        explore_movement = 'L';
      }else{
        explore_movement = 'R';
      }
    }else{
      explore_travel_until = time + 500*random(1, 10);
      explore_movement = 'F';
    }
  }
  if(explore_movement == 'S'){
    quick_turnR();
  }else if(explore_movement == 'F'){
    forward();
  }else if(explore_movement == 'L'){
    quick_turnL();
  }else{
    quick_turnR();
  }
}



void setup() {
  pinMode(MR_F,OUTPUT);
  pinMode(MR_B,OUTPUT);
  pinMode(ML_F,OUTPUT);
  pinMode(ML_B,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(EchoPinL, INPUT);
  pinMode(TrigPinL, OUTPUT);
  pinMode(EchoPinR, INPUT);
  pinMode(TrigPinR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  unsigned long distL = distanceL();
  unsigned long distR = distanceR();
  unsigned long time = millis();
  //Serial.println(distL);
  //Serial.println(distR);
  //delay(100);
  char val;
  char last_signal;
  if (Serial.available() > 0){
    val = Serial.read();
  }
  
  if(val == 'I'){
    init_flg = 1;
  }
  if(init_flg == 0){
    return;
  }
  if(val == 'S'){
    if(explore_state == 0){
       explore_state = 1;
       explore_movement = 'S';
       explore_travel_until = millis() + 6000;
    }
  }else if(val == 'F' or val == 'L' or val == 'R'){
    explore_state = 0;
    last_signal = val;
  }

  if(explore_state == 1){
    digitalWrite(LED_BUILTIN, HIGH);
    if(distL < D_close_threshold or distR < D_close_threshold){
      avoid(distL < D_close_threshold, distR < D_close_threshold);
    }else{
      explore(time);
    }
  }else{
    if(millis()-time_LED_toggled >=100){
      if (digitalRead(LED_BUILTIN) == false){
        digitalWrite(LED_BUILTIN, HIGH);
        time_LED_toggled = millis();
      }else{
        digitalWrite(LED_BUILTIN,LOW);
        time_LED_toggled = millis();
      }
    }
      switch (last_signal){
      case 'F':
        forward();
        break;
      case 'L':
        quick_turnL(255);
        break;
      case 'R':
        quick_turnR(255);
        break;
      case 'E':
        analogWrite(MR_F, 0);
        analogWrite(MR_B, 0);
        analogWrite(ML_F, 0);
        analogWrite(ML_B, 0);
        break;
      }
    
  }
  Serial.println(explore_travel_until);
  delay(10);
}

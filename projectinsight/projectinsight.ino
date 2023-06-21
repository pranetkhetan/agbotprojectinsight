#define lft_R_IS 4
#define lft_R_EN 2
#define lft_R_PWM 5
#define lft_L_IS 7
#define lft_L_EN 1
#define lft_L_PWM 3

#define rgt_R_IS 13
#define rgt_R_EN 12
#define rgt_R_PWM 6
#define rgt_L_IS 8
#define rgt_L_EN 11
#define rgt_L_PWM 10

int pwmspeed;
char command;

void setup(){
//LEFTMOTORDRIVER
pinMode(lft_R_IS,OUTPUT);
pinMode(lft_R_EN,OUTPUT);
pinMode(lft_R_PWM,OUTPUT);
pinMode(lft_L_IS,OUTPUT);
pinMode(lft_L_EN,OUTPUT);
pinMode(lft_L_PWM,OUTPUT);
digitalWrite(lft_R_IS,LOW);
digitalWrite(lft_L_IS,LOW);
digitalWrite(lft_R_EN,HIGH);
digitalWrite(lft_L_EN,HIGH);

//RIGHTMOTORDRIVER
pinMode(rgt_R_IS,OUTPUT);
pinMode(rgt_R_EN,OUTPUT);
pinMode(rgt_R_PWM,OUTPUT);
pinMode(rgt_L_IS,OUTPUT);
pinMode(rgt_L_EN,OUTPUT);
pinMode(rgt_L_PWM,OUTPUT);
digitalWrite(rgt_R_IS,LOW);
digitalWrite(rgt_L_IS,LOW);
digitalWrite(rgt_R_EN,HIGH);
digitalWrite(rgt_L_EN,HIGH);

//SERIALCOMMS
Serial.begin(9600);
delay(2000);
}

void forward(int pwmspeed){
analogWrite(rgt_R_PWM,pwmspeed);
analogWrite(rgt_L_PWM,0);
analogWrite(lft_R_PWM,pwmspeed);
analogWrite(lft_L_PWM,0);
}
void right(int pwmspeed){
analogWrite(rgt_R_PWM,pwmspeed);
analogWrite(rgt_L_PWM,0);
analogWrite(lft_R_PWM,0);
analogWrite(lft_L_PWM,pwmspeed);
}
void left(int pwmspeed){
analogWrite(rgt_R_PWM,0);
analogWrite(rgt_L_PWM,pwmspeed);
analogWrite(lft_R_PWM,pwmspeed);
analogWrite(lft_L_PWM,0);
}
void backward(int pwmspeed){
analogWrite(rgt_R_PWM,0);
analogWrite(rgt_L_PWM,pwmspeed);
analogWrite(lft_R_PWM,0);
analogWrite(lft_L_PWM,pwmspeed);
}

void stopmotors(){
analogWrite(rgt_R_PWM,0);
analogWrite(rgt_L_PWM,0);
analogWrite(lft_R_PWM,0);   
analogWrite(lft_L_PWM,0);              
}

void loop(){
  delay(5);
  if(Serial.available() > 0) {
    command = Serial.read();
    if(command == 'f'){
      forward(200);
    } else if(command == 'b') {
      backward(200);
    } else if(command == 'r') {
      right(200);
    } else if(command == 'l') {
      left(200);
    } else if(command == 's') {
      stopmotors();
    } else {
      stopmotors();
    }
  } else {
    stopmotors();
  }
      Serial.flush();
}

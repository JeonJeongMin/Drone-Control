//20190214 by Jeongmin

#include "mbed.h"

//경험적으로 수정 
#define ALPHA_VALUE 1.0000f
#define ROLL_KP     10
#define ROLL_KI     10
#define ROLL_KD     3
#define PITCH_KP     10
#define PITCH_KI     10
#define PITCH_KD     3
#define YAW_KP     10
#define YAW_KI     10
#define YAW_KD     3

#define ROLL_TARGET_ANGLE   0.000
#define PITCH_TARGET_ANGEL  0.000
#define YAW_TARGET_ANGLE    0.000 

#define MPU6050_ADDR     (0x68<<1) 
 
I2C i2c(PB_7, PB_6); 
Serial pc(SERIAL_TX, SERIAL_RX);
Serial ble(PA_9, PA_10);

Timer timer;

int16_t GyX,GyY,GyZ;

bool auto_aviation_mode = false;//
 
int main() {

    void initMPU6050();
    initMPU6050();

    pc.baud(115200);
    
    void calibAccelGyro();
    calibAccelGyro();
    
    timer.start();
    void initDT();
    initDT();
    
    //void accelNoiseTest();
    //accelNoiseTest();
    
    ble.baud(115200);
    void bleRxHandler(void);    
    ble.attach(bleRxHandler);
    
    void initMotorSpeed();
    initMotorSpeed();    
    
    while(1) {
        void readGyro();
        readGyro();
        
        void calcDT(); 
        calcDT();
        
        void calcGyroYPR();
        calcGyroYPR();
        
        void calcYPRtoStdPID();
        calcYPRtoStdPID();
        
        void calcMotorSpeed();
        calcMotorSpeed();
        
        void updateMotorSpeed(); 
        updateMotorSpeed();
        
        void autoAviation();
        if(auto_aviation_mode) //
            autoAviation();//
 
        void SendDataToProcessing();        
        static int cnt;
        cnt++;
        if(cnt%10==0)
            SendDataToProcessing();
    }     
}

void initMPU6050() {
    char data_write[2];   
    
    i2c.frequency(400000);    
    
    data_write[0] = 0x6B; //PWR_MGMT_1
    data_write[1] = 0x0; 
    i2c.write(MPU6050_ADDR, data_write, 2, false);
}

void readGyro() {
    char data_write[2];
    char data_read[6];
      
    data_write[0] = 0x43;
    i2c.write(MPU6050_ADDR, data_write, 1, true);
    i2c.read(MPU6050_ADDR, data_read, 6, false);
    
    GyX=data_read[0]<<8|data_read[1];
    GyY=data_read[2]<<8|data_read[3];
    GyZ=data_read[4]<<8|data_read[5];
}

double dt;
 
double gyro_angle_x,     gyro_angle_y,     gyro_angle_z;
extern double roll_output, pitch_output, yaw_output;
extern double 
  motorA_speed, motorB_speed, motorC_speed, motorD_speed;

void SendDataToProcessing() {
  
  
  pc.printf("DEL:");
  pc.printf("%lf", dt);
  pc.printf("#RPY:");
  pc.printf("%.2lf", gyro_angle_y);
  pc.printf(",");
  pc.printf("%.2lf", gyro_angle_x);
  pc.printf(",");
  pc.printf("%.2lf", gyro_angle_z);  
  pc.printf("#PID:");
  pc.printf("%.2lf", roll_output);
  pc.printf(",");
  pc.printf("%.2lf", pitch_output);
  pc.printf(",");
  pc.printf("%.2lf", yaw_output);  
  pc.printf("#A:");
  pc.printf("%.2lf", motorA_speed);  
  pc.printf("#B:");
  pc.printf("%.2lf", motorB_speed);  
  pc.printf("#C:");
  pc.printf("%.2lf", motorC_speed);  
  pc.printf("#D:");
  pc.printf("%.2lf", motorD_speed);

  pc.printf("\n\r"); 
  
}

double baseGyX, baseGyY, baseGyZ;

void calibAccelGyro() {  
  double sumGyX = 0, sumGyY = 0, sumGyZ = 0; 

  readGyro();
  
  for(int i=0;i<10;i++) {
    readGyro();    
    sumGyX += GyX; sumGyY += GyY; sumGyZ += GyZ;
    wait(0.1);
  }

  baseGyX = sumGyX / 10; 
  baseGyY = sumGyY / 10; 
  baseGyZ = sumGyZ / 10;   
}

unsigned long t_now;
unsigned long t_prev;

void initDT() {
  t_prev = timer.read_us();
}

void calcDT() {
  t_now = timer.read_us();
  dt = (t_now - t_prev)/1000000.0;
  t_prev = t_now;  
}

double gyro_x, gyro_y, gyro_z;

void calcGyroYPR() {  
  const double GYROXYZ_TO_DEGREES_PER_SEC = 131;
  
  gyro_x = (GyX - baseGyX)/GYROXYZ_TO_DEGREES_PER_SEC;
  gyro_y = (GyY - baseGyY)/GYROXYZ_TO_DEGREES_PER_SEC;
  gyro_z = (GyZ - baseGyZ)/GYROXYZ_TO_DEGREES_PER_SEC;
  
  gyro_angle_x += gyro_x * dt;
  gyro_angle_y += gyro_y * dt;
  gyro_angle_z += gyro_z * dt;
  
  extern double throttle;
  (throttle==0)?(gyro_angle_z=0):NULL;
  (throttle==0)?(gyro_angle_x=0):NULL;
  (throttle==0)?(gyro_angle_y=0):NULL; 
}

PwmOut motorA(D3);
PwmOut motorB(D10);
PwmOut motorC(D9);
PwmOut motorD(D11);

void accelNoiseTest() {        
    motorA.period_us(250);
    motorB.period_us(250);
    motorC.period_us(250);
    motorD.period_us(250);
    
    motorA.pulsewidth_us(25);
    motorB.pulsewidth_us(25); 
    motorC.pulsewidth_us(25);
    motorD.pulsewidth_us(25);
}

void stdPID( double& target_angle,
          double& current_angle,
          double& angular_velocity,          
          double& kp, 
          double& ki, 
          double& kd,
          double& iterm,
          double& output) {
  double error;
  double pterm, dterm;  
  
  error = target_angle - current_angle;
  
  pterm  =  kp * error;
  iterm +=  ki * error * dt;  
  dterm = -kd * angular_velocity;
  
  extern double throttle;
  (throttle==0)?(iterm=0):false;

  output = pterm + iterm + dterm;
}

double roll_target_angle = ROLL_TARGET_ANGLE;
double roll_prev_angle = 0.0;
double roll_kp = ROLL_KP; 
double roll_ki = ROLL_KI;
double roll_kd = ROLL_KD;
double roll_iterm;
double roll_output;

double pitch_target_angle = 0.0;
double pitch_prev_angle = 0.0;
double pitch_kp = PITCH_KP;
double pitch_ki = PITCH_KI;//1;//0.5;
double pitch_kd = PITCH_KD;//0.1;
double pitch_iterm;
double pitch_output;

double yaw_target_angle = 0.0;
double yaw_prev_angle = 0.0;
double yaw_kp = YAW_KP;
double yaw_ki = YAW_KI;//0.5;
double yaw_kd = YAW_KD;//0.1;
double yaw_iterm;
double yaw_output;

void calcYPRtoStdPID() {
  stdPID( roll_target_angle,
          gyro_angle_y,
          gyro_y,
          roll_kp, 
          roll_ki, 
          roll_kd,
          roll_iterm,
          roll_output);
  stdPID( pitch_target_angle,
          gyro_angle_x,
          gyro_x,
          pitch_kp, 
          pitch_ki, 
          pitch_kd,
          pitch_iterm,
          pitch_output);
  stdPID( yaw_target_angle,
          gyro_angle_z,
          gyro_z,
          yaw_kp, 
          yaw_ki, 
          yaw_kd,
          yaw_iterm,
          yaw_output);
}

double throttle = 0;
double motorA_speed, motorB_speed, motorC_speed, motorD_speed;

void calcMotorSpeed() {
  motorA_speed = (throttle == 0) ? 0:
    throttle + yaw_output + roll_output + pitch_output;
  motorB_speed = (throttle == 0) ? 0:
    throttle - yaw_output - roll_output + pitch_output;
  motorC_speed = (throttle == 0) ? 0:
    throttle + yaw_output - roll_output - pitch_output;
  motorD_speed = (throttle == 0) ? 0:
    throttle - yaw_output + roll_output - pitch_output;
    
  if(motorA_speed < 0) motorA_speed = 0; 
  if(motorA_speed > 250) motorA_speed = 250;
  if(motorB_speed < 0) motorB_speed = 0; 
  if(motorB_speed > 250) motorB_speed = 250;
  if(motorC_speed < 0) motorC_speed = 0; 
  if(motorC_speed > 250) motorC_speed = 250;
  if(motorD_speed < 0) motorD_speed = 0; 
  if(motorD_speed > 250) motorD_speed = 250;
}

enum {  
  HEAD1,  HEAD2,  HEAD3,  DATASIZE, CMD, 
  ROLL,   PITCH,  YAW,    THROTTLE,
  AUX,    CRCC,   PACKETSIZE,
};
uint8_t mspPacket[PACKETSIZE];
static int current_state=0;

void bleRxHandler() {        
    static uint32_t cnt;
                
    uint8_t mspData = ble.getc();
    if(mspData == '$') cnt = HEAD1;
    else cnt++;
    
    mspPacket[cnt] = mspData;
    
    if(cnt == (CMD+1)) {
        if(mspPacket[CMD] == 152) {
            if(!auto_aviation_mode) {
                auto_aviation_mode = true;
                current_state = 0;
            } else auto_aviation_mode = false;
            
            cnt = HEAD1;
        } else if(mspPacket[CMD] == 152) {
            cnt = HEAD1;
        }
    }
    if(auto_aviation_mode) {
        if(cnt == CRCC) cnt = HEAD1;
        
        return;
    }
    
    if(cnt == CRCC) {
        cnt = HEAD1;
        
        if(mspPacket[CMD] == 150) {
            throttle = mspPacket[THROTTLE];
            
            roll_target_angle = (mspPacket[ROLL] - 125);  
            pitch_target_angle = -(mspPacket[PITCH] - 125);  
            yaw_target_angle = -(mspPacket[YAW] - 125);
  
            if(roll_target_angle < -20) roll_target_angle = -20;
            else if(roll_target_angle > 20) roll_target_angle = 20;
            if(pitch_target_angle < -20) pitch_target_angle = -20;
            else if(pitch_target_angle > 20) pitch_target_angle = 20;  
            if(yaw_target_angle < -10) yaw_target_angle = -10;
            else if(yaw_target_angle > 10) yaw_target_angle = 10;       
            
             
            
                         
        }
    }
}

#define THROTTLE_MAX 250
#define THROTTLE_MIN 0

void initMotorSpeed() {    
    motorA.period_us(250);
    motorB.period_us(250);
    motorC.period_us(250);
    motorD.period_us(250);
    
    motorA.pulsewidth_us(THROTTLE_MIN);
    motorB.pulsewidth_us(THROTTLE_MIN);
    motorC.pulsewidth_us(THROTTLE_MIN); 
    motorD.pulsewidth_us(THROTTLE_MIN);
}

void updateMotorSpeed() {
    motorA.pulsewidth_us(motorA_speed); 
    motorB.pulsewidth_us(motorB_speed); 
    motorC.pulsewidth_us(motorC_speed); 
    motorD.pulsewidth_us(motorD_speed);  
}

void autoAviation() {        
   static unsigned long t_prev;
   static unsigned long t_interval=10;//ms
   
   unsigned long t_now = timer.read_ms();
   if(t_now - t_prev >= t_interval){
       t_prev=t_now;//
       current_state++; //100count/sec
       
       pc.printf("%d\n\r",current_state);
       if(0<=current_state && current_state <50){
         throttle = current_state*3.2;
         pc.printf("t:%lf\n\r",throttle);//1. throttle up 500 ms /10 = 50 st (0~50)
       } 
       else if (50<=current_state && current_state <250){
        pc.printf("t:%lf\n\r",throttle); //2. keep throttle for 2000 ms / 10 = 200 st (50~250)
       }
       
       else if (250<=current_state && current_state <400){ 
         pitch_target_angle=-6;
         //pc.printf("t:%lf\n\r",throttle);//3. throttle down 500 ms/ 10 = 50st (250~300) 
       }
       
       else if (400<=current_state && current_state <600){ 
         pitch_target_angle=3;
         //pc.printf("t:%lf\n\r",throttle);//3. throttle down 500 ms/ 10 = 50st (250~300) 
       }
       
       else if (600<=current_state && current_state <800){ 
         roll_target_angle=-5;
         //pc.printf("t:%lf\n\r",throttle);//3. throttle down 500 ms/ 10 = 50st (250~300) 
       }
       
       else if (800<=current_state && current_state <1000){ 
         roll_target_angle=3;
         //pc.printf("t:%lf\n\r",throttle);//3. throttle down 500 ms/ 10 = 50st (250~300) 
       }
       
      
       else if(1000<=current_state && current_state<1200){
         throttle = (1200-current_state)*3;
         
       }
       else if(1200<=current_state){
        
         throttle = 0;
         auto_aviation_mode = false;
       }
       
}

}


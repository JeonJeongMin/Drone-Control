#자율주행소스 (18-1경진대회 사용)
#상승 전진 우회전 전진 착지
#20190203 by Jeongmin
import serial
import struct
import time
import cv2

ser = serial.Serial('COM9',115200)
print("connected to: " + ser.portstr)

ser.write(b'AT+COND43639D8898D')
print("connected to: AIR0012")

HEAD1 = 36 # ->'$'
HEAD2 = 60 # 60 '<'  62 '>'
CMD = 150 # 150 CMD 151 EMERGENCY 152 AUTO aviation
ROLL= 125 # target_angle
PITCH = 125
YAW = 125
THROTTLE = 0
PACKETSIZE = 8

data = struct.pack('>8B',HEAD1, HEAD2, CMD, ROLL, PITCH, YAW, THROTTLE, PACKETSIZE)
ser.write(data)

while True:
    key=input('방향을 입력하세요. :')
    if key=='z':
        break
    if key=='q':
        THROTTLE=THROTTLE-250
    elif key=='c':
        ser.write(b'AT+COND43639D8898D')
        print("connected to: AIR0012")
    elif key=='w':
    	THROTTLE=THROTTLE+30
    elif key == 's':
        THROTTLE=THROTTLE-30
        
    elif key=='a':
        while THROTTLE>0:
            THROTTLE=THROTTLE-40
            if THROTTLE<0:
                 THROTTLE=0
            data = struct.pack('>8B',HEAD1, HEAD2, CMD, ROLL, PITCH, YAW, THROTTLE, PACKETSIZE)
            ser.write(data)
            print('전송')
            time.sleep(0.3)
        THROTTLE=THROTTLE-250

    elif key=='i':
        PITCH=PITCH+2
    elif key=='k':
        PITCH=PITCH-2
    elif key=='j':
        ROLL=ROLL-2
    elif key=='l':
        ROLL=ROLL+2
    elif key=='r':
        flag = 2
        while True:
            cv2.namedWindow('title',cv2.WINDOW_NORMAL)
            key = cv2.waitKey(60)

            if key == 27:
                THROTTLE=THROTTLE-250
                break
            if key == ord('q'):
                THROTTLE=THROTTLE-250
                break
            elif key==ord('w'):
                THROTTLE = THROTTLE+30
            elif key==ord('j'):
                ROLL=ROLL-2

            if flag<6: #상승
                if flag==3:
                    ROLL=ROLL-4
                    
                THROTTLE=THROTTLE+62

            elif flag<9: #상승반동 및 유지
                THROTTLE=THROTTLE-15

            elif flag<25: #전진
                if flag==12:
                    PITCH=PITCH+14

            elif flag<30: #전진반동
                if flag==25:
                    PITCH=PITCH-18
                    THROTTLE=THROTTLE+10

            elif flag<43: #우회전
                if flag==30:
                    ROLL=ROLL+14
                
            elif flag<48: #우회전 반동
                if flag==43:
                    ROLL=ROLL-18
                    THROTTLE=THROTTLE+15

            elif flag<61: #전진
                if flag==48:
                    PITCH=PITCH+18
                    THROTTLE=THROTTLE+15
                
            elif flag<66: #전진 반동
                if flag==61:
                    PITCH=PITCH-18
                THROTTLE=THROTTLE-50

            elif flag<68: #하강
                THROTTLE=THROTTLE+20

            elif flag<69:
                THROTTLE=THROTTLE-30
            
            else:
                THROTTLE=0
                ROLL=125
                PITCH=125
                
            if flag>10 and flag<38:

                if (flag%4) == 0:
                    #PITCH=PITCH+2
                    #ROLL=ROLL+2
                    THROTTLE=THROTTLE+19
                elif (flag%4) == 1:
                    #PITCH=PITCH+2
                    #ROLL=ROLL+2
                    THROTTLE=THROTTLE-20
                elif (flag%4) == 2:
                    #PITCH=PITCH-2
                    #ROLL=ROLL-2
                    THROTTLE=THROTTLE+19
                elif (flag%4) == 3:
                    #PITCH=PITCH-2
                    #ROLL=ROLL-2
                    THROTTLE=THROTTLE-20
                
            flag=flag+1
            
            if THROTTLE<0:
                 THROTTLE=0
            elif THROTTLE>250:
                THROTTLE=250

            elif key == ord('z'):
                THROTTLE=0
                ROLL=125
                PITCH=125
            
            print(flag, 'throttle: ',THROTTLE,'pitch(앞): ', PITCH-125,'roll(오른): ', ROLL-125)
            data = struct.pack('>8B',HEAD1, HEAD2, CMD, ROLL, PITCH, YAW, THROTTLE, PACKETSIZE)
            ser.write(data)
            time.sleep(0.05)
        cv2.destroyAllWindows()
    
    elif key =='z':
        THROTTLE=0
        ROLL=125
        PITCH=125
    
    if THROTTLE<0:
         THROTTLE=0
    elif THROTTLE>250:
        THROTTLE=250
    data = struct.pack('>8B',HEAD1, HEAD2, CMD, ROLL, PITCH, YAW, THROTTLE, PACKETSIZE)
    ser.write(data)
    #print(THROTTLE)

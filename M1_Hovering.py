import serial
import struct
import time
import cv2

ser = serial.Serial('COM9',115200)
print("connected to: " + ser.portstr)

ser.write(b'AT+COND43639DE43EE')
print("connected to: AIR0020")

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
        ser.write(b'AT+COND43639DE43EE')
        print("connected to: AIR0020")
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
        flag = 0
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
                if flag==2:
                    ROLL=ROLL-2
                    #PITCH=PITCH+2
                    
                THROTTLE=THROTTLE+40

            elif flag<8: #상승반동 및 유지
                THROTTLE=THROTTLE-20

            elif flag<10:
                THROTTLE=THROTTLE+9
                if flag==9:
                    ROLL=ROLL-2

            elif flag<12:
                THROTTLE=THROTTLE-10
                
            elif flag>12 and flag <34:
                if flag==13:
                    ROLL=ROLL+2
                    PITCH=PITCH-2
                if flag==15:
                    THROTTLE=THROTTLE+10
                    
                if flag==18:
                    PITCH=PITCH+2
                if flag==23:
                    ROLL=ROLL+2

                if flag ==26:
                    ROLL=ROLL-2
                
                if (flag%4) ==0:
                    THROTTLE=THROTTLE+10
                elif (flag%4) ==1:
                    THROTTLE=THROTTLE-5     
                elif (flag%4) ==2:
                    THROTTLE=THROTTLE-5     
                elif (flag%4) ==3:
                    THROTTLE=THROTTLE+10     
                    
            elif flag<37:
                THROTTLE=THROTTLE-30
                
            elif flag<40:
                THROTTLE = THROTTLE+20
                
            elif flag<44:
                THROTTLE=THROTTLE-40

            elif flag<47:
                THROTTLE=THROTTLE+20

            else:
                THROTTLE=0
                break

            if flag>12:
                if (flag%4) ==0:
                    ROLL=ROLL+2
                    PITCH=PITCH+2
                elif (flag%4) ==1:
                    ROLL=ROLL-2
                    PITCH=PITCH-2
                elif (flag%4) ==2:
                    ROLL=ROLL-2
                    PITCH=PITCH-2    
                elif (flag%4) ==3:
                    ROLL=ROLL+2
                    PITCH=PITCH+2 
                
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
            time.sleep(0.15)
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

#블루투스를 통한 drone제어
#20190203 by Jeongmin
import serial
import struct
import time
import cv2

ser = serial.Serial('COM3',115200)
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
    print('z:종료,q:throttle=0, c:reconnect, w/s:throttle조절, a:safe landing')
    print('r:Enter생략(opencv창실행), i/k:PITCH조절, j/l:ROLL조절 ')
    key=input('명령을 입력하세요.:')
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
        PITCH=PITCH+1
    elif key=='k':
        PITCH=PITCH-1
    elif key=='j':
        ROLL=ROLL-1
    elif key=='l':
        ROLL=ROLL+1
    elif key=='r':
        flag = 0

        #드론의 초기상태에 따라 ROLL,PITCH 값 조절(기울기 방지)
        ROLL=ROLL-3
        PITCH=PITCH+2

        while True:
            #cv2.namedWindow('title',cv2.WINDOW_NORMAL)
            keymap = cv2.imread('keymap.jpg')
            cv2.imshow('title',keymap)
            key = cv2.waitKey(60)

            if key == 27:
                THROTTLE=THROTTLE-250
                break
            if key == ord('q'):
                THROTTLE=THROTTLE-250
            elif key==ord('i'):
                PITCH=PITCH+2
            elif key==ord('k'):
                PITCH=PITCH-2
            elif key==ord('j'):
                ROLL=ROLL-2
            elif key==ord('l'):
                ROLL=ROLL+2
            
            elif key==ord('w'):
                THROTTLE = THROTTLE+30
            elif key==ord('s'):
                THROTTLE = THROTTLE-30

            '''
            if (flag%4) == 0:
                PITCH=PITCH+2
                ROLL=ROLL-2
            elif (flag%4) == 1:
                PITCH=PITCH+2
                ROLL=ROLL+2
            elif (flag%4) == 2:
                PITCH=PITCH-2
                ROLL=ROLL+2
            elif (flag%4) == 3:
                PITCH=PITCH-2
                ROLL=ROLL-2
            '''

            flag=flag+1
            if THROTTLE<0:
                 THROTTLE=0
            elif THROTTLE>250:
                THROTTLE=250

            elif key == ord('z'):
                THROTTLE=0
                ROLL=125
                PITCH=125
            
            print('throttle: ',THROTTLE,'pitch(앞): ', PITCH-125,'roll(오른): ', ROLL-125)
            data = struct.pack('>8B',HEAD1, HEAD2, CMD, ROLL, PITCH, YAW, THROTTLE, PACKETSIZE)
            ser.write(data)
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

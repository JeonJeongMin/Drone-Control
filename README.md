# 드론경진대회 소스
 - 18년도 드론경진대회 (일반조종, 호버링, 자율)소스입니다.

 ## 사용된 HW
  - 메인보드 : Cortex-M4 (F303K8) 
  - PL2303 USB to UART 모듈
  - HM10 블루투스 모듈(드론1, 외부1)
 
 ## 소스코드
 ### Drone 내부소스

 #### Cortex-M4(Drone.cpp)
  - 블루투스 통신을 통해 들어온 외부의 비행정보 읽음
  - PID제어를 통한 각 4개의 Motor제어
  - Mbed.com 에서 제공하는 Compiler로 컴파일 후 생성된 파일을 USB로 드론에 넣음

 ### Drone 외부소스

 #### Drone(Serial+BT)
  - Drone과 Bluetooth통신
  - Protocol 포함
  - 명령어를 통한 ROLL,PITCH,THROTTLE 제어

 #### M1_Hovering
  - 실험을 통한 호버링 소스
  - safe landing(key:a)

 #### M2_Auto Driving
  - 실험을 통한 자율주행(상승, 전진, 우회전, 전진, 착지)
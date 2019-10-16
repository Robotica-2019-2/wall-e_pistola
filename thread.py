#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveSteering
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import InfraredSensor, ColorSensor, TouchSensor
from time import sleep
import time, logging, threading

# INPUT_1 - InfraredSensor
# INPUT_2 - TouchSensor
# INPUT_3
# INPUT_4 - ColorSensor

# OUTPUT_A
# OUTPUT_B - MoveTank (Motor Esquerdo)
# OUTPUT_C - MoveTank (Motor Direito)
# OUTPUT_D - MediumMotor (Motor de Tiro)

sleep_time = 0.3
# default sleep timeout in sec
DEFAULT_SLEEP_TIMEOUT_IN_SEC = 0.05

def sound(message):
  sound = Sound()
  sound.speak(message)

def oneShooter():
        tank_shooter = MediumMotor(OUTPUT_D)
        tank_shooter.on_for_rotations(SpeedPercent(75), 4)

# tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# def walk():
#   t=0
#   steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
#   steering_drive.on(1, 50)
#   t=t+1
#   print('\n')
#   print(t)
#   if(t>10):
#     steering_drive.off()

def walkOnly():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # steering_drive.on_for_rotations(0, SpeedPercent(25), 2)
  steering_drive.on_for_seconds(0, SpeedPercent(50), 5)

def walkRight():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(-20, SpeedPercent(50), 2)

def turnRight():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(-100, SpeedPercent(50), 2)

def turnLeft():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(100, SpeedPercent(50), 1)

def walkLeft():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(20, SpeedPercent(50), 2)

def walkBack():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(100, SpeedPercent(50), 3)

def top_left_channel_1_action(state):
    print("top left on channel 1: %s" % state)

def bottom_right_channel_4_action(state):
    print("bottom right on channel 4: %s" % state)

# def detect_robot():
#     infrared_sensor = InfraredSensor(INPUT_1)
#     infrared_sensor.mode = 'IR-SEEK'
#     canal = 1
#     while True:
#       dis = infrared_sensor.heading_and_distance(channel=canal)
#       if(dis[1] is not None and dis[0] < 5 and dis[0] > 5):
#         oneShooter()

#       sound('Distance')
#       time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
      # print(str(dis))

def walk_shooter_strategy():
    global stopMotorSensor
    global stopColorSensor
    global stopProxSensor
    global stopInfraredSensor
    global infrared_sensor
    shots=3
    infrared_sensor.mode = 'IR-PROX'
    while True:
        if(stopProxSensor):
          break  
        distance = infrared_sensor.value()
        if distance < 5:
              stopMotorSensor=True
              stopColorSensor=True
              time.sleep(0.5)
              turnRight()
              stopMotorSensor=False
              stopColorSensor=False
              t2 = threading.Thread(target=onlyWalkWorker)
              t2.start()
              # t3 = threading.Thread(target=detectBlackWorker)
              # t3.start()

def detect_black():
    global  stopColorSensor
    global  stopInfraredSensor
    global  stopMotorSensor
    global  stopProxSensor

    color_sensor = ColorSensor(INPUT_4)
    color_sensor.mode = 'COL-REFLECT'
    while True:    
      if(stopColorSensor):
        break
      time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
      if(color_sensor.value() < 20):
        #DEU PRETO
        stopInfraredSensor=True
        stopMotorSensor=True
        stopProxSensor=True
        time.sleep(0.5)
        walkBack()
        stopInfraredSensor=False
        stopMotorSensor=False
        stopProxSensor=False
        time.sleep(0.5)
        t2 = threading.Thread(target=onlyWalkWorker)
        t2.start()
        # t3 = threading.Thread(target=detectBlackWorker)
        # t3.start()
        t4 = threading.Thread(target=walk_shooter_strategy)
        t4.start()
    print(str(color_sensor.value()))

# threading ---------------------------

def robotDetectWorker():
    global stopColorSensor
    global stopInfraredSensor
    global stopMotorSensor
    global stopProxSensor
    global infrared_sensor

    canal = 1
    while True:
      if(stopInfraredSensor):
        break
      infrared_sensor.mode = 'IR-SEEK'     
      dis = infrared_sensor.heading_and_distance(4)
      if(dis[1] is not None and dis[0] > -5 and dis[0] < 5 and dis[1] < 30):
          oneShooter()
      else:
        infrared_sensor.mode = 'IR-PROX'
        distance = infrared_sensor.value()
        if distance <= 30:
          stopMotorSensor=True
          stopColorSensor=True
          time.sleep(0.5)
          turnRight()
          time.sleep(0.5)
          stopMotorSensor=False
          stopColorSensor=False
          t2 = threading.Thread(target=onlyWalkWorker)
          t2.start()
          # t3 = threading.Thread(target=detectBlackWorker)
          # t3.start()
              

def turnRightWorker():
    global sleep_time
    while True:
      turnRight()
      print(sleep_time)
      time.sleep(sleep_time)
      sleep_time=0.3

def onlyWalkWorker():
  global stopColorSensor
  global stopInfraredSensor
  global stopMotorSensor
  while True:
    if(stopMotorSensor):
        break
    walkOnly()

def detectBlackWorker():
  detect_black()

def deathTread(t2):
  time.sleep(2)
  t2.join()

ts = TouchSensor(INPUT_2)

print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
print("#################################")
while not ts.is_pressed:
  time.sleep(0.2)

def main():
  global stopColorSensor
  global stopInfraredSensor
  global stopMotorSensor
  global stopProxSensor
  global infrared_sensor
  
  infrared_sensor = InfraredSensor(INPUT_1)

  stopColorSensor=False
  stopInfraredSensor=False
  stopMotorSensor=False
  stopProxSensor=False

  t1 = threading.Thread(target=robotDetectWorker)
  t1.start() 

  t2 = threading.Thread(target=onlyWalkWorker)
  t2.start()

  # t3 = threading.Thread(target=detectBlackWorker)
  # t3.start()

  #t4 = threading.Thread(target=walk_shooter_strategy)
  #t4.start()
  
main()


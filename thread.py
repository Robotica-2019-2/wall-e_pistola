#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveSteering
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import InfraredSensor, ColorSensor
from time import sleep
import time, logging, threading


# default sleep timeout in sec
DEFAULT_SLEEP_TIMEOUT_IN_SEC = 0.05

def sound(message):
  sound = Sound()
  sound.speak(message)

def oneShooter(shots):
    # if shots > 0:
        tank_shooter = MediumMotor(OUTPUT_D)
        tank_shooter.on_for_rotations(SpeedPercent(75), 4)

# tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

def walk(time):
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(0, SpeedPercent(75), 2)

def walkRight():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(-20, SpeedPercent(75), 2)

def turnRight():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(-100, SpeedPercent(50), 0.3)

def turnLeft():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(100, SpeedPercent(50), 1)

def walkLeft():
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(20, SpeedPercent(50), 2)

def top_left_channel_1_action(state):
    print("top left on channel 1: %s" % state)

def bottom_right_channel_4_action(state):
    print("bottom right on channel 4: %s" % state)

def detect_robot():
    infrared_sensor = InfraredSensor(INPUT_1)
    infrared_sensor.mode = 'IR-SEEK'
    canal = 1
    while True:
      dis = infrared_sensor.heading_and_distance(channel=canal)
      if(dis[0] < 5 and dis[0] > 5):
        oneShooter()

      sound('Distance')
      time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
      # print(str(dis))

def walk_shooter_strategy():
    infrared_sensor = InfraredSensor(INPUT_1)
    infrared_sensor.mode = 'IR-PROX'
    count = 0

    shots=3
    while True:
        distance = infrared_sensor.value()
        # print(distance)
        if distance > 50:
            count = count + 1
            turnRight()
        else:
            oneShooter(shots)
            shots = shots - 1

def detect_black():
    # Connect infrared and touch sensors to any sensor ports
    color_sensor = ColorSensor(INPUT_4)
    # logging.info("color sensor connected: %s" % str(color_sensor.connected))
    color_sensor.mode = 'COL-REFLECT'
    while True:
      time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
      if(color_sensor.value() < 20):
        sound('BLACK!')
      else:
        sound('NOT BLACK!')
    print(str(color_sensor.value()))

def walk_shooter_strategy():
    infrared_sensor = InfraredSensor(INPUT_1)
    infrared_sensor.mode = 'IR-SEEK'
    count = 0

    shots=3
    while True:
        distance = infrared_sensor.value()
        print(distance)
        if distance > 50:
            count = count + 1
            turnRight()
        else:
            oneShooter(shots)
            shots = shots - 1

def detect_black():
      while True:
        time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
        if(color_sensor.value() < 20):
          sound('BLACK!')
        else:
          sound('NOT BLACK!')
      print(str(color_sensor.value()))

# threading ---------------------------

def turnRightWorker():
    while True:
      turnRight()
      time.sleep(1)


def shooterDetectWorker():
    infrared_sensor = InfraredSensor(INPUT_1)
    infrared_sensor.mode = 'IR-SEEK'
    count = 0
    shots=3
    while True:
      distance = infrared_sensor.value()
      if distance <= 50:
          oneShooter(shots)
          shots = shots - 1
          time.sleep(1)

def robotDetectWorker():
    infrared_sensor = InfraredSensor(INPUT_1)
    infrared_sensor.mode = 'IR-SEEK'
    
    shots=3
    canal = 2
    while True:
      dis = infrared_sensor.heading_and_distance(channel=canal)
      beacon = infrared_sensor.beacon(channel=canal)
      print(dis)
      time.sleep(1)
      if(dis[1] is not None and dis[0] > -5 and dis[0] < 5 and dis[1] < 30):
          print(beacon)
          # print(beacon)
          # oneShooter(shots)
          # shots = shots - 1
          time.sleep(1)

# t1 = threading.Thread(target= turnRightWorker)
#t2 = threading.Thread(target= shooterDetectWorker)
t3 = threading.Thread(target=robotDetectWorker)
# robotDetectWorker()
# t1.start()
# t2.start()
t3.start()
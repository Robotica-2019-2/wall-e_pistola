#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveSteering
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import InfraredSensor, ColorSensor, TouchSensor
from time import sleep
import time, logging, threading

#---------- Documentação -------------#

# INPUT_1 - InfraredSensor
# INPUT_2 - TouchSensor
# INPUT_3
# INPUT_4 - ColorSensor

# OUTPUT_A
# OUTPUT_B - MoveTank (Motor Esquerdo)
# OUTPUT_C - MoveTank (Motor Direito)
# OUTPUT_D - MediumMotor (Motor de Tiro)

#-------------------------------------- AÇÕES ---------------------------------------#

sleep_time = 0.3
DEFAULT_SLEEP_TIMEOUT_IN_SEC = 0.05

def sound(message):
  sound = Sound()
  sound.speak(message)

def oneShooter():
        tank_shooter = MediumMotor(OUTPUT_D)
        tank_shooter.on_for_rotations(SpeedPercent(75), 4)

def walkSeconds(direction, velocity, seconds):
      steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_seconds(direction, SpeedPercent(velocity), seconds)

def walkRotations(direction, velocity, rotations):
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  steering_drive.on_for_rotations(direction, SpeedPercent(velocity), rotations)

#-------------------------------------- MÉTODOS DE MOVIMENTO ---------------------------------------#

def walkOnly():
  walkSeconds(0,50,5)

def walkRight():
  walkRotations(-20,50,2)

def turnRight():
  walkRotations(-100,50,2)

def turnLeft():
  walkRotations(100,50,2)

def walkLeft():
  walkRotations(20,50,2)

def walkBack():
  walkRotations(-100,50,3)

#-------------------------------------- WORKERS ---------------------------------------#

def proxDetectWorker():
    global stopMotorSensor
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
              time.sleep(0.5)
              turnRight()
              stopMotorSensor=False
              t2 = threading.Thread(target=onlyWalkWorker)
              t2.start()

def turnRightWorker():
    global sleep_time
    while True:
      turnRight()
      print(sleep_time)
      time.sleep(sleep_time)
      sleep_time=0.3

def robotDetectWorker():
    global stopInfraredSensor
    global stopMotorSensor
    # global stopProxSensor
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
          time.sleep(0.5)
          turnRight()
          time.sleep(0.5)
          stopMotorSensor=False
          t2 = threading.Thread(target=onlyWalkWorker)
          t2.start()

def onlyWalkWorker():
      global stopInfraredSensor
  global stopMotorSensor
  while True:
    if(stopMotorSensor):
        break
    walkOnly()

#-------------------------------------- MAIN ---------------------------------------#

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
  global stopInfraredSensor
  global stopMotorSensor
  # global stopProxSensor
  global infrared_sensor
  
  infrared_sensor = InfraredSensor(INPUT_1)

  stopInfraredSensor=False
  stopMotorSensor=False
  # stopProxSensor=False

  t1 = threading.Thread(target=robotDetectWorker)
  t1.start() 

  t2 = threading.Thread(target=onlyWalkWorker)
  t2.start()

  #t4 = threading.Thread(target=proxDetectWorker)
  #t4.start()
  
main()
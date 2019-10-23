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
CANAL = 4

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

def walkBack():
  walkRotations(-100,50,3)

def stopThread(motor,patrol,infra):
  global stopMotorSensor
  global stopPatrol
  global stopInfraredSensor
  stopMotorSensor = motor
  stopPatrol = patrol
  stopInfraredSensor = infra

def startThread(motor, patrol, infra):
  global stopMotorSensor
  global stopPatrol
  global stopInfraredSensor
  
  if(motor):
    stopMotorSensor = False
    t1 = threading.Thread(target=onlyWalkWorker)
    t1.start() 
  if(patrol):
    stopPatrol = False
    t2 = threading.Thread(target=patrolEdgeWorker)
    t2.start() 
  if(infra):
    stopInfraredSensor = False
    t3 = threading.Thread(target=robotDetectWorker)
    t3.start()

#-------------------------------------- WORKERS ---------------------------------------#

def robotDetectWorker():
    global stopInfraredSensor
    global infrared_sensor
    
    while True:
      if(stopInfraredSensor):
        break
      infrared_sensor.mode = 'IR-SEEK'     
      dis = infrared_sensor.heading_and_distance(CANAL)

      if(dis[1] is not None and dis[0] > -15 and dis[0] < 15 and dis[1] < 60):
        oneShooter()
      else:
        infrared_sensor.mode = 'IR-PROX'
        distance = infrared_sensor.value()
        if distance <= 15:
          stopThread(True, True, False)
          walkSeconds(-100,35,1.37) 
          dis = infrared_sensor.heading_and_distance(CANAL)
          while (dis[1] is not None and dis[0] > -15 and dis[0] < 15 and dis[1] < 60):
              time.sleep(0.5)
              oneShooter()
              time.sleep(0.5)
              dis = infrared_sensor.heading_and_distance(CANAL)
          stopThread(False, True, False)
          startThread(True, False, False)
    
def onlyWalkWorker():
  global countWalk
  while True and stopPatrol and countWalk < 15:
    if(stopMotorSensor):
        break
    walkSeconds(0,50,5)
    countWalk=countWalk+1
  if(countWalk>=15):
    stopThread(True,True,False)
    walkSeconds(-100,35,1.37)
    walkSeconds(100,35,1.37)
    startThread(True,False,False)
    countWalk = 0
    
def patrolEdgeWorker():
  global countPatrol
  while True and stopMotorSensor and countPatrol < 5:
    if(stopPatrol):
      break
    walkSeconds(-100,35,1.37)
    walkSeconds(100,35,1.37)
    countPatrol=countPatrol+1
  if(countPatrol>=5):
    stopThread(True,True,False)
    startThread(True,False,False)

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
  global stopMotorSensor
  global stopPatrol
  global stopInfraredSensor
  global countWalk
  global countPatrol
  stopMotorSensor=False
  stopPatrol=False
  stopInfraredSensor=False
  countWalk = 0
  countPatrol = 0
  global infrared_sensor
  infrared_sensor = InfraredSensor(INPUT_1)
  
  stopThread(False, False, False)
  startThread(False, True, True)

main()
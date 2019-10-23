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

def stopThread(motor, patrol, infra, giro):
  global stopMotorSensor
  global stopPatrol
  global stopInfraredSensor
  global stopGiro
  stopMotorSensor = motor
  stopPatrol = patrol
  stopInfraredSensor = infra
  stopGiro = giro

def startThread(motor, patrol, infra, giro):
  if(motor):
    t1 = threading.Thread(target=onlyWalkWorker)
    t1.start() 
  if(patrol):
    t2 = threading.Thread(target=patrolEdgeWorker)
    t2.start() 
  if(infra):
    t3 = threading.Thread(target=robotDetectWorker)
    t3.start()
  if(giro):
    t4 = threading.Thread(target=giroWorker)
    t4.start()

#-------------------------------------- WORKERS ---------------------------------------#

def giroWorker():
  global stopGiro
    while True:
      if(stopGiro):
        break
      walkSeconds(-100,100,1.7)

def robotDetectWorker():
    global stopInfraredSensor
    global infrared_sensor
    
    while True:
      if(stopInfraredSensor):
        break
      infrared_sensor.mode = 'IR-SEEK'     
      dis = infrared_sensor.heading_and_distance(CANAL)

      if(dis[1] is not None and dis[0] > -30 and dis[0] < 30):
        stopThread(True, True, False, False)
        startThread(False,False,False,True)
        while(dis[0] > -15 and dis[0] < 15 and dis[0] > 60):
          stopThread(True, True, False, True)              
          time.sleep(0.5)
          oneShooter()
          time.sleep(0.5)
          dis = infrared_sensor.heading_and_distance(CANAL)
      else:
        infrared_sensor.mode = 'IR-PROX'
        distance = infrared_sensor.value()
        if distance <= 15:
          stopThread(True, True, False, True)
          walkSeconds(-100,35,1.37) 
          dis = infrared_sensor.heading_and_distance(CANAL)
          while (dis[1] is not None and dis[0] > -15 and dis[0] < 15 and dis[1] < 60):
              time.sleep(0.5)
              oneShooter()
              time.sleep(0.5)
              dis = infrared_sensor.heading_and_distance(CANAL)
          stopThread(False, True, False, True)
          startThread(True, False, False, False)
    
def onlyWalkWorker():
  global count
  count = 0
  while True and stopPatrol and count < 15:
    if(stopMotorSensor):
        break
    walkSeconds(0,50,5)
    count=count+1
  if(count>=15):
    stopThread(True,True,False,True)
    walkSeconds(-100,35,1.37)
    walkSeconds(100,35,1.37)
    startThread(True,False,False,False)
    
def patrolEdgeWorker():
  global count
  count = 0
  while True and stopMotorSensor and count < 5:
    if(stopPatrol):
      break
    walkSeconds(-100,35,1.37)
    walkSeconds(100,35,1.37)
    count=count+1
  if(count>=5):
    stopThread(True,True,False,True)
    startThread(True,False,False,False)

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
  global stopGiro
  stopMotorSensor=False
  stopPatrol=True
  stopInfraredSensor=False
  stopGiro=True
  global infrared_sensor
  infrared_sensor = InfraredSensor(INPUT_1)

  startThread(True, True, True, False)
  stopThread(False, True, False, True)

main()
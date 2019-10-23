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
CANAL_CONST = 4

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

def dataThread():
  global disProx
  global disSeek
  while True:
    infrared_sensor.mode = 'IR-SEEK'     
    disSeek = infrared_sensor.heading_and_distance(CANAL_CONST)
    infrared_sensor.mode = 'IR-PROX'     
    disProx = infrared_sensor.value()

def stopThread(motor,prox,infra):
  global stopMotorSensor
  global stopInfraredSensor
  stopMotorSensor = motor
  stopInfraredSensor = infra

def startThread(motor, prox, infra):
  if(motor):
    t1 = threading.Thread(target=robotDetectWorker)
    t1.start() 
  if(infra):
    t2 = threading.Thread(target=onlyWalkWithStopWorker)
    t2.start()
#-------------------------------------- MÉTODOS DE MOVIMENTO ---------------------------------------#

def walkOnly():
  walkSeconds(0,50,5)

def walkRight():
  walkRotations(-20,50,2)

def turnRight():
  walkSeconds(100,50,1)
  # walkRotations(-100,50,1)

def turnLeft():
  walkRotations(-100,50,1)

def walkLeft():
  walkRotations(20,50,2)

def walkBack():
  walkRotations(-100,50,3)

#-------------------------------------- WORKERS ---------------------------------------#

def turnRightWorker():
    global sleep_time
    while True:
      turnRight()
      print(sleep_time)
      time.sleep(sleep_time)
      sleep_time=0.3

def modoCaca():
    global disSeek
    if(disSeek[1] is not None):
      if(disSeek[1] < 10):
        stopThread(True, True, False)

def modoPatrulha():
    global stopMotorSensor
    while True:
      if(stopMotorSensor):
        break
      walkSeconds(-100,35,1)
      if(disProx<20):
            

def onlyWalkWorker():
  global stopInfraredSensor
  global stopMotorSensor
  while True:
    if(stopMotorSensor):
        break
    walkOnly()

# movimentação com paradas
def onlyWalkWithStopWorker():
  global stopInfraredSensor
  global stopMotorSensor
  while True:
    if(stopMotorSensor):
        break
    time.sleep(0.2)
    walkRotations(0,100,2)
    time.sleep(0.2)

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
      
  # t = threading.Thread(target=dataThread)
  # t.start()

  # global stopInfraredSensor
  # global stopMotorSensor
  # global infrared_sensor
  
  # infrared_sensor = InfraredSensor(INPUT_1)

  # stopInfraredSensor=False
  # stopMotorSensor=False

  # t1 = threading.Thread(target=modoPatrulha)
  # t1.start()

  # t2 = threading.Thread(target=onlyWalkWithStopWorker)
  # t2.start()


main()
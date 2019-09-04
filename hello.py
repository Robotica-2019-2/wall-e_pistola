#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import InfraredSensor  

def sound():
  sound = Sound()
  sound.speak('Welcome to the E V 3 dev project!')

tank_drive = MediumMotor(OUTPUT_D)

def oneShooter():
  tank_drive.on_for_rotations(SpeedPercent(75), 4)

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

def walk():
  tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), 15)

def walkRight():
  tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(75), 10)

def walkLeft():
  tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)

time = 3
i = 0
#for i in range(time):
#   walk()

#walkRight()
#walkLeft()
#oneShooter()

#walk()
#walkRight()
#oneShooter()

#walkLeft()
#oneShooter()


# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor()

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

while not ir.value():
    distance = ir.value()
    print(distance)
    if distance < 60:
        tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), 10)
    else:
        oneShooter()

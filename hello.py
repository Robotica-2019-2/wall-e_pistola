#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import InfraredSensor
from time import sleep
import logging

def planoB():
    s = 3
    i = 0
    for i in range(s):
      walk()

    walkRight()
    walkLeft()
    oneShooter()

    walk()
    walkRight()
    oneShooter()

    walkLeft()
    oneShooter()

def sound(message):
  sound = Sound()
  sound.speak(message)

def oneShooter(shots):
    if shots > 0:
        tank_shooter = MediumMotor(OUTPUT_D)
        tank_shooter.on_for_rotations(SpeedPercent(75), 4)
    else:
        print("No Bullets!")
        sound("No Bullets!")

# tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

def walk(time):
  # tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), time)
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # drive in a turn for 10 rotations of the outer motor
  steering_drive.on_for_rotations(0, SpeedPercent(75), 2)

def walkRight():
  #   tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), time)
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # drive in a turn for 10 rotations of the outer motor
  steering_drive.on_for_rotations(-20, SpeedPercent(75), 2)

def turnRight():
  #   tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), time)
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # drive in a turn for 10 rotations of the outer motor
  steering_drive.on_for_rotations(-100, SpeedPercent(50), 0.4)

def turnLeft():
  #   tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), time)
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # drive in a turn for 10 rotations of the outer motor
  steering_drive.on_for_rotations(100, SpeedPercent(50), 1)

def walkLeft():
  #   tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), time)
  steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
  # drive in a turn for 10 rotations of the outer motor
  steering_drive.on_for_rotations(20, SpeedPercent(50), 2)

def top_left_channel_1_action(state):
    print("top left on channel 1: %s" % state)

def bottom_right_channel_4_action(state):
    print("bottom right on channel 4: %s" % state)

def walk_shooter_strategy():
    count = 0
    # Connect infrared and touch sensors to any sensor ports
    ir = InfraredSensor(INPUT_1)

    # Put the infrared sensor into proximity mode.
    ir.mode = 'IR-PROX'
    shots=3
    while True:
        distance = ir.value()
        print(distance)
        if distance > 50:
            count = count + 1
            turnRight()
        else:
            oneShooter(shots)
            shots = shots - 1

walk_shooter_strategy()
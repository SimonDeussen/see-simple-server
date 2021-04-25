#!/usr/bin/env micropython

from time import sleep, time
import sys
import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from ev3dev2.button import Button
import urequests
import ujson

IP_ADDRESS = "ENTER IP ADDRESS"
SERVER = "http://" + IP_ADDRESS + ":5000/log_ev3_standard"

if IP_ADDRESS == "ENTER IP ADDRESS":
    raise Exception("does not work without ip address.")


buttons = Button()
move = MoveTank(OUTPUT_A, OUTPUT_D)
spkr = Sound()
motor_1 = LargeMotor(OUTPUT_A)
motor_2 = LargeMotor(OUTPUT_D)

motor_1_path = []  # in rad
motor_2_path = []  # in rad

motor_1_path.append(motor_1.position)
motor_2_path.append(motor_2.position)

times_motor_1 = []
times_motor_2 = []

spkr.speak('Press a button')
while True:
    if buttons.left:
        move.on_for_seconds(SpeedPercent(30), SpeedPercent(40), 2.2, block=False)

    elif buttons.up:
        move.on_for_seconds(SpeedPercent(40), SpeedPercent(40), 2.2, block=False)

    elif buttons.right:
        move.on_for_seconds(SpeedPercent(40), SpeedPercent(30), 2.2, block=False)

    if (motor_1.is_running):
        motor_1_path.append((motor_1.position * math.pi) / 180.0)
        times_motor_1.append(time())
    if (motor_2.is_running):
        motor_2_path.append((motor_2.position * math.pi) / 180.0)
        times_motor_2.append(time())

    if (motor_1.is_holding and motor_2.is_holding):

        data_length = min(len(motor_1_path), len(motor_2_path))

        data = {'motor_1': [], 'motor_2': []}

        for motor, time in zip(motor_1_path, times_motor_1):
            data['motor_1'].append({'motor_pos': motor, 'time': time})

        for motor, time, in zip(motor_2_path, times_motor_2):
            data['motor_2'].append({'motor_pos': motor, 'time': time})

        urequests.post(SERVER, json=ujson.dumps(data))

        spkr.speak('Motion completed')
        break

    # don't let this loop use 100% CPU
    sleep(0.001)

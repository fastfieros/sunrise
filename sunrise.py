#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

RGB = (11,13,15)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(RGB[0], GPIO.OUT)
GPIO.setup(RGB[1], GPIO.OUT)
GPIO.setup(RGB[2], GPIO.OUT)

Rp = GPIO.PWM(RGB[0], 120)  # channel=25 frequency=50Hz
Gp = GPIO.PWM(RGB[1], 120)  # channel=25 frequency=50Hz
Bp = GPIO.PWM(RGB[2], 120)  # channel=25 frequency=50Hz

Rp.start(0)
Gp.start(0)
Bp.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            Rp.ChangeDutyCycle(dc)
            Gp.ChangeDutyCycle(dc)
            Bp.ChangeDutyCycle(dc)
            time.sleep(0.025)
        for dc in range(100, -1, -5):
            Rp.ChangeDutyCycle(dc)
            Gp.ChangeDutyCycle(dc)
            Bp.ChangeDutyCycle(dc)
            time.sleep(0.025)
except KeyboardInterrupt:
    pass

Rp.stop()
Gp.stop()
Bp.stop()

GPIO.cleanup()

#!/usr/bin/env python

from flask import Flask, render_template, url_for
import time
import RPi.GPIO as GPIO



app=Flask(__name__)

@app.route('/')
def getIndex():

    return render_template("index.html")

@app.route('/change/<name>/<newval>')
def change(name, newval):

    print name, newval
    if name == "red":
        Rp.ChangeDutyCycle(int(newval))

    elif name == "green":
        Gp.ChangeDutyCycle(int(newval))

    elif name == "blue":
        Bp.ChangeDutyCycle(int(newval))

    return "%s, %s"%(name,newval)

if __name__ == "__main__":

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

        app.run(host='0.0.0.0', port=80, debug=True)

        Rp.stop()
        Gp.stop()
        Bp.stop()

        GPIO.cleanup()

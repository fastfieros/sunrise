#!/usr/bin/env python

from flask import Flask, render_template, url_for, request, make_response
import time, sys, Queue 
#import RPi.GPIO as GPIO
from sunrise import *
from dateutil import parser
import datetime

app=Flask(__name__)
strip = RGBstrip()

@app.route('/')
def getIndex():
    global alarmtime
    global alarm

    at = None
    hours = 0
    minutes = 0
    if alarmtime is not None:
        #delt = alarmtime - datetime.datetime.now()
        #seconds = delt.total_seconds()
        seconds = alarm.secondsLeft()
        hours = int(seconds / 3600)
        minutes = int( (seconds % 3600 ) / 60)

    resp = make_response( render_template("alarm.html", request=request, 
                           at=alarmtime, hours=hours, 
                           minutes=minutes))

    resp.cache_control.no_cache = True
    return resp

@app.route('/change/<name>/<newval>')
def change(name, newval):

    x = 255 - int(newval) 
    print name, x
    strip.update(name, x)

    return "%s, %s"%(name,newval)

@app.route('/setRGB/<r>/<g>/<b>')
def setRGB(r,g,b):
    strip.r = int(r, 16)
    strip.g = int(g, 16)
    strip.b = int(b, 16)
    strip.setRgb()

    return strip.current() 

@app.route('/alarm')
def getAlarm():
    return getIndex()

@app.route('/alarm/<timestr>')
def setAlarm(timestr):
    global alarmtime
    global alarm

    if timestr == "disable":
        alarmtime = None
        if alarm != None:
            alarm.__del__()
        alarm = None
        return "Disabled"

    alarmtime = parser.parse(timestr, fuzzy=True)

    #if past day - then set it for tommorow!!
    if datetime.datetime.now() > alarmtime:
        alarmtime = alarmtime.replace(day=datetime.datetime.now().day+1)
        
    if alarm != None:
        alarm.__del__()

    alarm = timer(alarmtime, strip.alarm)
    alarm.start()
    print "alarm set for ", alarm.secondsLeft(), "seconds from now."
    return str(alarmtime)


if __name__ == "__main__":

    global alarmtime
    global alarm

    alarmtime = None
    alarm = None

    app.run(host='0.0.0.0', port=8080, debug=True)

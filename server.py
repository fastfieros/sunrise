#!/usr/bin/env python

from flask import Flask, render_template, request, make_response
from sunrise import *
from timer import timer, Alarm

app = Flask(__name__)
strip = RGBstrip()

@app.route('/')
def getIndex():
    global alarm

    at = None
    hours = 0
    minutes = 0
    if alarm is not None:
        at = alarm.alarmtime
        seconds = alarm.secondsLeft()
        if seconds is not None:
            hours = int(seconds / 3600)
            minutes = int( (seconds % 3600 ) / 60)

    resp = make_response( render_template("alarm.html", 
        request=request, at=at, dimmer=int(round(strip.dimFactor * 100)),
        hours=hours, minutes=minutes))

    resp.cache_control.no_cache = True
    return resp

@app.route('/setRGB/<r>/<g>/<b>')
def setRGB(r,g,b):
    strip.fade(int(r,16),
               int(g,16),
               int(b,16),
               0.5)

    return strip.current() 

@app.route('/dimmer')
def getDimmer():
    return str(round(strip.dimFactor * 100))

@app.route('/dimmer/<newdim>')
def setDimmer(newdim):
    newval = float(newdim)
    if newval >= 0 and newval <= 1:
        strip.dimFactor = newval
        strip.apply()
        return "Set dimmer to %f."%newval
    else:
        return "dimfactor must be between 0 and 1"

@app.route('/cycle')
def startCycle():
    strip.cycle()
    return "started cycle"

@app.route('/alarm')
def getAlarm():
    return getIndex()

@app.route('/alarm/<timestr>')
def setAlarm(timestr):
    global alarm

    if timestr == "disable":
        alarm.cleanup()
        alarm = None
        return "Disabled"

    alarm = Alarm(timestr, strip.sunrise)
    print "alarm set for ", alarm.secondsLeft(), "seconds from now."
    return str(alarm.nextAlarmDate)


if __name__ == "__main__":

    global alarm
    alarm = None

    app.run(host='0.0.0.0', port=80, debug=True)

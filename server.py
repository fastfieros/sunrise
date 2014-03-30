#!/usr/bin/env python

from flask import Flask, render_template, url_for
import time, sys, Queue 
#import RPi.GPIO as GPIO
from sunrise import *

app=Flask(__name__)
#strip = RGBstrip()

@app.route('/')
def getIndex():

    return render_template("index.html")

@app.route('/change/<name>/<newval>')
def change(name, newval):

    x = 255 - int(newval) 
    print name, x
    #strip.update(name, x)

    return "%s, %s"%(name,newval)

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)

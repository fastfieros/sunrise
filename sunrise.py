#!/usr/bin/env python

import time, os
#import RPi.GPIO as GPIO
import serial
import threading
from datetime import datetime, timedelta

class RGBstrip():


    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyAMA0")
        except:
            self.ser = file("/tmp/noserial", "w")

        self.r = 0;
        self.g = 0
        self.b = 0;

    def update(self, name, value):

        value = int(value)
        if value > 255 or value < 0:
            print "Bad value: ", value
            return

        if "red" in name:
            self.r = value

        elif "green" in name:
            self.g = value

        elif "blue" in name:
            self.b = value

        else:
            print "Unknown name: ",name
            return

        print "Set ",name," to ",value, ": ",self.r,self.g,self.b
        self.setRgb()

    def setRgb(self):
        for c in (self.r,self.g,self.b):
            if c >255 or c<0:
                print "Invalid value: ",c
                return;

        self.ser.write("%d,%d,%d\n"%(
            256-self.g,
            255-self.r,
            255-self.b))
        print("%d,%d,%d\n"%(self.g,self.r,self.b))

    def current(self):
        return "#%02X%02X%02X"%(self.r,self.g,self.b)

    def alarm(self):
        self.r = 1
        self.g = 0
        self.b = 0
        self.setRgb()
        print "ALARM!"

    def cleanup(self):

        self.ser.close()

    def __del__(self):
        self.cleanup()

class timer(threading.Thread):

    def __init__(self, timeout=None, callback=None):
        self.timeout = timeout or datetime.now()
        self.done = False
        self.callback = callback
        threading.Thread.__init__(self)

    def run(self):
        print "running"
        while not self.done:
            now = datetime.now()
            print self.secondsLeft(), "s left, sleeping 1"

            if now > self.timeout:
                self.done = True

                print "about to call: ", self.callback
                if self.callback:
                    self.callback()
            else:
                time.sleep(1)

    def secondsLeft(self):
        return (self.timeout - datetime.now()).total_seconds()

    def __del__(self):
        self.done = True

def callback():
    print "HAY."

if __name__ == "__main__":

    now = datetime.now() 
    print "now: ", now
    when = now + timedelta(seconds=5)
    print "setting alarm for: ",when
    t = timer(when, callback)
    t.start()



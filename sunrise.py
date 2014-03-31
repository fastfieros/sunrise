#!/usr/bin/env python

import time, os
#import RPi.GPIO as GPIO
import serial
import threading
from datetime import datetime, timedelta

class timer(threading.Thread):

    def __init__(self, timeout=None, callback=None, res=1):
        self.timeout = timeout or datetime.now()
        self.done = False
        self.callback = callback
        self.resolution = res
        threading.Thread.__init__(self)

    def run(self):
        print "running"
        while not self.done:
            now = datetime.now()
            #print self.secondsLeft(), "s left, sleeping 1"

            if now > self.timeout:
                self.done = True

                if self.callback:
                    self.callback()
            else:
                time.sleep(self.resolution)

    def secondsLeft(self):
        return (self.timeout - datetime.now()).total_seconds()

    def kill(self):
        self.done = True

    def __del__(self):
        self.kill()

class RGBstrip():


    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyAMA0")
        except:
            self.ser = file("/tmp/noserial", "w")

        self.r = 0;
        self.g = 0
        self.b = 0;

        self.timer = None

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
        secondsPerMinute = 60
        minutesOfFade = 25
        self.fade(255, 128, 0, secondsPerMinute * minutesOfFade)

    def fade(self, new_r, new_g, new_b, seconds):
        if self.timer != None:
            self.timer.kill()

        self.last_r = self.r
        self.last_g = self.g
        self.last_b = self.b

        self.delta_r = new_r - self.r
        self.delta_g = new_g - self.g
        self.delta_b = new_b - self.b

        self.currentStep = 0
        self.numSteps = max(
                abs(self.delta_r), 
                abs(self.delta_g), 
                abs(self.delta_b))

        
        self.secondsPerStep = float(seconds) / float(self.numSteps)

        self._stepFade()

    def _stepFade(self):

        #decrement numsteps
        self.currentStep += 1

        #set colors to correct output
        percentage = float(self.currentStep) / float(self.numSteps)

        self.r = self.last_r + int(percentage * self.delta_r)
        self.g = self.last_g + int(percentage * self.delta_g)
        self.b = self.last_b + int(percentage * self.delta_b)

        self.setRgb()

        # set up the next timeout, if we're not done
        if self.numSteps > self.currentStep:
            self.timer = timer(
                    timeout = datetime.now() + timedelta(seconds=self.secondsPerStep), 
                    callback = self._stepFade, 
                    res = self.secondsPerStep).start()
        

    def cleanup(self):

        self.ser.close()

    def __del__(self):
        self.cleanup()


def callback():
    print "HAY."

if __name__ == "__main__":

    #now = datetime.now() 
    #print "now: ", now
    #when = now + timedelta(seconds=5)
    #print "setting alarm for: ",when
    #t = timer(when, callback)
    #t.start()

    s = RGBstrip()
    s.fade(255,255,128,60)

#!/usr/bin/env python

import time, os, random
#import RPi.GPIO as GPIO
import serial
import threading
from datetime import datetime, timedelta
from timer import timer

secondsPerMinute = 60

class RGBstrip():

    minutesOfFade = 20

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyAMA0")
        except:
            self.ser = file("/tmp/noserial", "w")

        self.r = 0;
        self.g = 0
        self.b = 0;

        self.dimFactor = 1.

        self.fadeTimer = None
        self.fadeCallback = None
        self.fadeStartTime = datetime.now()
        self.fadeSeconds = None

    def changeCompnent(self, name, value):

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

        #print "Set ",name," to ",value, ": ",self.r,self.g,self.b
        self.apply()

    def apply(self):
        for c in (self.r,self.g,self.b):
            if c >255 or c<0:
                print "Invalid value: ",c
                return;

        cmd = ("%d,%d,%d\n"%(
            256-int(round(self.dimFactor * self.g)),
            255-int(round(self.dimFactor * self.r)),
            255-int(round(self.dimFactor * self.b))
            ))
        self.ser.write(cmd)
        #print(cmd)

    def current(self):
        return "#%02X%02X%02X"%(self.r,self.g,self.b)

    def sunrise(self):
        self._sunrise_step_0()

    def _sunrise_step_0(self):
        # first 1/4 time, fade to dim red 
        self.fade( 32,  0, 0, 
                secondsPerMinute * self.minutesOfFade / 4, 
                self._sunrise_step_1)

    def _sunrise_step_1(self):
        # then fade to bright orange
        self.fade(255, 34, 0, 
                secondsPerMinute * self.minutesOfFade / 4, 
                self._sunrise_step_2)

    def _sunrise_step_2(self):
        # Then fade to white
        self.fade(255,255,255, 
                secondsPerMinute * self.minutesOfFade / 2)

    def stopFade(self):
        if self.fadeTimer != None:
            self.fadeTimer.kill()

        self.fadeTimer = None


    def fade(self, new_r, new_g, new_b, seconds, callback=None):

        #If a fade is going, stop it now!
        self.stopFade()

        self.fadeCallback = callback
        self.fadeStartTime = datetime.now()
        self.fadeSeconds = seconds

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

        #keep a reasonable server load
        if seconds < 1:
            self.numSteps = min(
                    self.numSteps,
                    int(round(seconds * 64)))

        if self.numSteps == 0: 
            self.numSteps = 1
        
        self.secondsPerStep = float(seconds) / float(self.numSteps)

        self._stepFade()

    def _stepFade(self, final=False):

        #Figure out what step we're on
        secondsSoFar = (datetime.now() - self.fadeStartTime).total_seconds()
        prog = min(secondsSoFar / self.fadeSeconds, 1)

        self.currentStep = int(round(prog * self.numSteps))
        #print ("%3.2f%%, step %d/%d"%(prog, self.currentStep, self.numSteps))

        #set colors to correct output
        self.r = self.last_r + int(prog * self.delta_r)
        self.g = self.last_g + int(prog * self.delta_g)
        self.b = self.last_b + int(prog * self.delta_b)
        self.apply()

        # Are we done yet?
        if self.currentStep < self.numSteps:
            # if not, set up the next timeout
            self.fadeTimer = timer(
                    timeout = datetime.now() + timedelta(seconds=self.secondsPerStep), 
                    callback = self._stepFade, 
                    res = self.secondsPerStep)
            self.fadeTimer.start()

        elif not final:
            #This is the second-to-last step!

            # make sure we get to do the last step (because we
            # don't want rounding or CPU delays to make us stop at 96.7%..
            self._stepFade(final=True)

        else:
            # call the callback if there is one, then reset it so
            # it doens't get called again if it's not set in the future
            self.fadeCallback and self.fadeCallback()

        
    def cycle(self):

        #select new color by adding random delta to each
        # exisiting component
        r = max(min(self.r + random.randint(-255,255), 255), 0)
        g = max(min(self.g + random.randint(-255,255), 255), 0)
        b = max(min(self.b + random.randint(-255,255), 255), 0)
        print "Cycling to %02X%02X%02X"%(r,g,b)

        #Fade to the new color slowly, callback is ourself!
        #self.fade(r,g,b, 16, self.cycle)
        self.fade(r,g,b, 3, self.cycle)


    def cleanup(self):
        self.ser.close()

    def __del__(self):
        self.cleanup()



if __name__ == "__main__":

    s = RGBstrip()
    s.fade(255,255,128,10)

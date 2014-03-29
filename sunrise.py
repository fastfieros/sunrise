#!/usr/bin/env python

import time, os
#import RPi.GPIO as GPIO
import serial

class RGBstrip():


    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0")
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

        self.ser.write("%d,%d,%d\n"%(self.g,self.r,self.b))
        print("%d,%d,%d\n"%(self.g,self.r,self.b))

    def cleanup(self):

        self.ser.close()

    def __del__(self):
        self.cleanup()


if __name__ == "__main__":
    pass

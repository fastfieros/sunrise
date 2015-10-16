#!/usr/bin/env python

import threading
import time
from datetime import datetime, timedelta
from dateutil import parser

class timer(threading.Thread):

    def __init__(self, timeout=None, callback=None, res=1):

        self.timeout = timeout or datetime.now()
        self.callback = callback
        self.resolution = res

        self.done = False
        threading.Thread.__init__(self)

        #print ("timer created for %s"%repr(self.timeout))

    def run(self):
        #print "timer running"
        while not self.done:
            now = datetime.now()
            #print self.secondsLeft(), "s left, sleeping 1"

            if now > self.timeout:
                self.done = True

                #print "timer finished"
                if self.callback:
                    #print "calling", self.callback
                    self.callback()

                return

            else:
                time.sleep(self.resolution)

        #print "timer killed"

    def secondsLeft(self):
        """Return the number of seconds remaining in the timer, as a float"""
        return (self.timeout - datetime.now()).total_seconds()

    def kill(self):
        """Stop the child thread"""
        self.done = True

    def __del__(self):
        """Dtor. calls kill"""
        self.kill()

class Alarm():

    def __init__(self, timestr, usercallback, days=(True, True, True, True, True, False, False)):

        alarmDate = parser.parse(timestr, fuzzy=True)
        print ("parsed timstr to: ", alarmDate)

        self.alarmtime = alarmDate.time()
        self.nextAlarmDate = alarmDate
        self.daysActive = days;
        self.usercallback = usercallback
        self.timerForNextAlarm = None

        allfalse = True
        for i in days:
            if days[i]:
                allfalse = False

        if allfalse:
            #There are no set days!
            print "No days set.."
            return None;

        self.setNextTimer()

    def setNextTimer(self):

        #start with todays date, at the scheduled alarmtime 
        now = datetime.now() 
        self.nextAlarmDate = now.replace(
                hour=self.alarmtime.hour, 
                minute=self.alarmtime.minute,
                second=self.alarmtime.second)

        # if that is in the past, change it to tomorrow
        if now > self.nextAlarmDate:
            self.nextAlarmDate = self.nextAlarmDate + timedelta(days=1)

        #increment day until we find one where the user wants an alarm
        while self.daysActive[self.nextAlarmDate.weekday()] == False:
            self.nextAlarmDate = self.nextAlarmDate + timedelta(days=1)

        #kill any previously running alarm timer (shouldn't need this?)
        self.cleanup()

        print "setting next alarm for ", self.nextAlarmDate
        self.timerForNextAlarm = timer(self.nextAlarmDate, self.callback, res=30)
        self.timerForNextAlarm.start()

    def secondsLeft(self):
        if self.timerForNextAlarm:
            return self.timerForNextAlarm.secondsLeft()
        else:
            return None

    def cleanup(self):
        if self.timerForNextAlarm != None:
            self.timerForNextAlarm.kill()

    def callback(self):

        self.setNextTimer()
        self.usercallback()


def callback():
    print "HAY."

if __name__ == "__main__":

    now = datetime.now() 
    print "now: ", now
    when = now + timedelta(seconds=5)
    print "setting alarm for: ",when
    #t = timer(when, callback)
    #t.start()

    a = Alarm(str(when), callback)
    print "wait.. "

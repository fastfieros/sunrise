#!/usr/bin/env python

import threading
import time
from datetime import datetime, timedelta

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

def callback():
    print "HAY."

if __name__ == "__main__":

    now = datetime.now() 
    print "now: ", now
    when = now + timedelta(seconds=5)
    print "setting alarm for: ",when
    t = timer(when, callback)
    t.start()

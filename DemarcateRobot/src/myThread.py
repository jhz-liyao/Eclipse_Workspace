# -*- coding: utf-8 -*-
#################################################################################
# Group:   JHZ-Robot
# File :   RobotEgo.py
# Date :   2016-01-07
# Discription :
#          robotEgo.
#################################################################################

import time 
import threading

class Robot_thread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, ag, func,tname):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.arg = ag
        self.name=tname
        self.running = True
        self.function =func
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " + self.threadID
        print self.arg
        #while self.running:
         #   self.function(self.arg)
        #if not self.running:
         #   thread.exit()
        self.function(self.arg) 
        #threading.Thread.exit()
        print "Exiting " + self.threadID
    def stop(self):
        print "ready stoping "+ self.threadID
        print self.arg




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
import socket, traceback
import json
import sqlite3
#from tcp_connect import *
from myThread import *
from protocol import *

#*****************************************
# Class:   Steps
# Date :
# Discription:
#*****************************************
class Steps(object):
    def __init__(self, _stp, _stn, _target_position, _model, _type, _auto, _proc):
        self.step = _stp
        self.station = _stn
        self.target_position = _target_position
        self.model = _model
        self.type = _type
        self.auto = _auto
        self.process = _proc        
#*****************************************
# Class:   Stations
# Date :
# Discription:
#*****************************************
class Stations(object):
    def __init__(self, _stn, _occupied, _location_a, _location_b, _location):
        self.station = _stn
        self.occupied = _occupied
        self.location_a = _location_a
        self.location_b = _location_b
        self.location = _location
        self.robot_id = ''

#*****************************************
# Class:   Process
# Date :
# Discription:
#*****************************************
class Process(object):
    def __init__(self, _proc, _stp_sequence, _location):
        self.station = _stn
        self.step_sequence = _stp_sequence

#*****************************************
# Class:   Point
# Date :
# Discription:
#*****************************************
class Point(object):
    def __init__(self, _x, _y, _th):
        self.x = float(_x)
        self.y = float(_y)
        self.th = float(_th)

#*****************************************
# Class:   Robots
# Date :
# Discription:
#*****************************************
class Robots(object):
    def __init__(self, r_id, ip, port):
        self.robot_id = r_id
        self.label_id = ''
        self.station = ''
        self.step = ''
        self.location = '0,0,0'#Point(0,0,0)
        self.odometer =''
        self.cmd = ''   #指令 队列
        self.process = ''
        self.action = ''
        self.roomnum =''
        self.running = True
        self.auto = False
        self.locationARR=[]
        self.mainthread = 0
        self.rcvthread = 0         
        self.connectTCP = tcp_connect(ip, port, self)
        self.connectCMD = 0  

#*****************************************
# Class:   tcp_connect
# Date :
# Discription:
#*****************************************
class tcp_connect(object):
    def __init__(self, ip, port, r_id):
        self.ip = ip
        self.port = port
        self.robot_id = r_id
        self.connectTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectTCP.settimeout(2)
        self.connectTCP.connect((ip, port))        
        #set_keepalive_linux(self.connectTCP)
    def send(self,data):
        try:
            ret = self.connectTCP.send(data)
        except  socket.error as err:
            print 'send-error:'+str(err)
            print '######################1#########################'            
            self.reconnect()
            get_robot_connection_state(self.robot_id)
            time.sleep(1)
            ret = self.connectTCP.send(data)
        return ret
    def recv(self,num):
        rcv = ''
        try:
            rcv = self.connectTCP.recv(num)
        except socket.error as err: 
            if err[0] != 'timed out':
                print '###################2########################'
                print 'recv-error:'+str(err)
                rcv = err
                self.reconnect()                
                get_robot_connection_state(self.robot_id)
        return rcv
    def reconnect(self):
        try:
            print 'reconnecting'
            self.connectTCP.close()
            self.connectTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connectTCP.settimeout(2)
            self.connectTCP.connect((self.ip, self.port))            
        except socket.error as err:
            print 'reconnect-error'+str(err)
    def oob_detect(self):
        try:
            self.connectTCP.send('x',socket.MSG_OOB)
            return 1
        except socket.error as err:
            print 'OOB-error:'+str(err)
            self.reconnect()
            return -1
    def clean(self):
        try:
            while(1):
                rcv = self.connectTCP.recv(1)
                if not rcv:
                    break
        except:
            print 'clean'


    
        
    

       

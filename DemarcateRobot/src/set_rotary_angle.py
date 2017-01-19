#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
import serial 
import sqlite3
import time
import json
import os
import cgi, cgitb
# print "Content-type:text/html\r\n\r\n"
#     #print str(os.environ)
#     data= cgi.FieldStorage()
#     for key in list(data):
#         print str(key)+':'+str(data.getvalue(key))
#     
 
# Create your views here.
def set_rotary_angle(rotary_id,motor_angle1,motor_angle2):
    
    UART_COM = ''
    if rotary_id == '1':
        COMx = 'com1'
    if rotary_id == '2':
        COMx = 'com2'
    if rotary_id == '3':
        COMx = 'com3'
    if rotary_id == '4':
        COMx = 'com4'
    if rotary_id == '5':
        COMx = 'com5'
    if rotary_id == '6':
        COMx = 'com6'
        
    if rotary_id == 'FL0':
        sqlHandle = sqlite3.connect('E:\LiyaoProject\eclipse_workspace\DemarcateRobot\src\Robot.db')
        sqlInterface = sqlHandle.cursor()
        sql = 'insert into test (flag,datetime)values(1,datetime(\'now\')) '
        sqlHandle.execute(sql)
        sqlHandle.commit()
        sqlHandle.close()
        print 'success'
        return
        
    try:
        UART_COM = serial.Serial(COMx,9600)
        print COMx
    except:
        return 'open %s error'%COMx
    try: 
        COM_SET = ['1','2','3','4','5','6']        
        UART_COM.flushInput()
        UART_COM.flushOutput()
        if rotary_id in COM_SET:
            #-----------motor1---------
            angle = float(motor_angle1)
            motor_id =1
            print angle
            angle = int(angle*1000/78)
            if angle<0:
                dr ='\x00'
                angle_1 = -angle/256
                angle_2 = -angle%256
            else:
                dr = '\x02'
                angle_1 = angle/256
                angle_2 = angle%256            
            print 'm',motor_id
            m_id = chr(int(motor_id))            
            strCMD = '\xfd\x02'+m_id+dr+'\x4b\x20\x00'+chr(angle_1)+chr(angle_2)+'\x00\x00\x00\x00\xf8'
            UART_COM.write(strCMD)
            time.sleep(0.1)
            UART_COM.write(strCMD)            
            #-----------motor2---------
            time.sleep(0.1)
            angle = float(motor_angle2)
            motor_id =2
            print angle
            angle = int(angle*1000/78)
            if angle<0:
                dr ='\x02'
                angle_1 = -angle/256
                angle_2 = -angle%256
            else:
                dr = '\x00'
                angle_1 = angle/256
                angle_2 = angle%256            
            print 'm',motor_id
            m_id = chr(int(motor_id))            
            strCMD = '\xfd\x02'+m_id+dr+'\x4b\x20\x00'+chr(angle_1)+chr(angle_2)+'\x00\x00\x00\x00\xf8'
            UART_COM.write(strCMD)
            time.sleep(0.1)
            UART_COM.write(strCMD)            
        time.sleep(0.1)
        #ret = UART_COM.read(60)        
        rcv = ''#ret.split(',')
        j_s = {}
        for s in rcv:
            a = s.split(':')
            if len(a)==2:
                a[0]
                j_s[a[0]]=a[1]    
        return str(j_s)        
    except:
        #print 'set_rotary_angle:error'
        pass
    try:
        UART_COM.close()
    except:
        print 'b'    
#处理传入参数
print 'a'
while 1:
    set_rotary_angle('FL0',45,45)
    print 'A'
    set_rotary_angle('1',45,45)
    set_rotary_angle('2',45,45)
    set_rotary_angle('3',45,45)
    set_rotary_angle('4',45,45)
    set_rotary_angle('5',45,45)
    set_rotary_angle('6',45,45)
    time.sleep(20)
    print 'B'
    set_rotary_angle('1',-45,-45)
    set_rotary_angle('2',-45,-45)
    set_rotary_angle('3',-45,-45)
    set_rotary_angle('4',-45,-45)
    set_rotary_angle('5',-45,-45)
    set_rotary_angle('6',-45,-45)
    time.sleep(20)
    set_rotary_angle('1',0,0)
    set_rotary_angle('2',0,0)
    set_rotary_angle('3',0,0)
    set_rotary_angle('4',0,0)
    set_rotary_angle('5',0,0)
    set_rotary_angle('6',0,0)
    time.sleep(20)
    break
print 'over'

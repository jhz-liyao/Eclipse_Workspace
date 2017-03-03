#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
import serial 
import sqlite3
import time
import json
import os
import cgi, cgitb

def set_rotary_angle(COMx, motor_offset, motor_speed): 
    try:
        UART_COM = serial.Serial(COMx, 9600)
        print COMx
    except:
        return 'open %s error'%COMx
    try:       
        UART_COM.flushInput()
        UART_COM.flushOutput()
        #-----------motor1---------
        motor_dir = 0
        if(motor_offset >= 0):
            motor_dir = 1
        else:
            motor_offset = -motor_offset
            motor_dir = 0 
        offset = float(motor_offset) 
        print offset
        integer = int(offset)
        decimals = int((offset - integer)*10)
#         while 1:
#             if((decimals - int(decimals) <  0.000001) and (decimals - int(decimals) >  -0.000001)):
#                 break
#                 
#             decimals = decimals * 10.0 
#         decimals = int(decimals)
        #m_id = chr(int(motor_id))            
        #strCMD = '\xfd\x01'+chr(motor_dir)+chr(integer>>8) + chr(integer|0xff) + chr(decimals >> 8) + chr(decimals|0xff) + chr(motor_speed) + '\x00\xf8'
        #运动到中点
        if motor_offset > 0.49 and motor_offset < 0.51 and motor_speed == 50:
            strCMD = '\xfd\x03\x00\x00\xf8'
        else:
            strCMD = '\xfd\x01'+chr(motor_dir)+chr(integer>>8)+ chr(integer&0xff) + chr(decimals >> 8) + chr(decimals&0xff) + chr(motor_speed) + '\x00\xf8'
        
        UART_COM.write(strCMD)
        TimeOut_Cnt = 10  #超时计时5S
        print "Start : %s" % time.ctime()
        while True:
            time.sleep(0.5)
            TimeOut_Cnt-=1
            ret = ''
            ret += str(UART_COM.read(UART_COM.inWaiting()))
            #ret = ret.decode('gb2312')
            if(ret.find('OK') > 0):
                print 'OK'
                break
            elif(TimeOut_Cnt == 0):
                print 'TIMEOUT'
                break 
        print "End : %s" % time.ctime()
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

data= cgi.FieldStorage()
data1 = data.getvalue('com', 'com2')
data2 = data.getvalue('offset', '0')
data3 = data.getvalue('speed', '0')
  
# data1 = 'com6'
# data2 = 0.5
# data3 = 50


offset = float(data2)
offset = round(offset,1)
speed = int(data3)
print "Content-type:text/html"
print                               # 空行，告诉服务器结束头部
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>滑台运动控制程序</title>' 
print '</head>'
print '<body>'
print '参数1:'+str(data1)+'</br>参数2:' + str(data2) + '</br>参数3:' + str(data3) + '</br>'
print '位置:'+str(offset)+'</br>速度:' + str(speed) +'</br>'
print set_rotary_angle(data1, offset, speed)  
print '</body>'
print '</html>'

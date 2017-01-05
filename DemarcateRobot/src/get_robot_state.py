#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
import sqlite3
import json
from cgi import parse_qs,escape
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('F:\pyserver')
from serverTool import *

def app(robot_id,cmd,robot_ip):
    #--------------指令请求插入------------------------------------
    sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
    sqlInterface = sqlHandle.cursor()    
    sql = 'SELECT * FROM robot_list WHERE robot_id = "%s" ' % (robot_id)
    sqlInterface.execute(sql)
    ret = sqlInterface.fetchall() 
    if len(ret)==0:
        sql = 'INSERT INTO robot_list(robot_id,robot_ip,robot_port,cmd) values ("%s", "%s", "%s", "%s")'
        data = (robot_id,robot_ip,9010,cmd['robot_state']['process'])
        sql = sql % data 
        #print sql        
        sqlHandle.execute(sql)
        sqlHandle.commit()
    elif len(ret) == 1:
        sql = 'update robot_list set cmd = "%s" where robot_id = "%s"'
        data = (str(cmd['robot_state']['process']),robot_id)
        sql = sql % data 
        #print sql        
        sqlHandle.execute(sql)
        sqlHandle.commit()
    sqlHandle.close()
    #--------------状态信息反馈------------------------------------
    step = {}
    ResponseInfo = ''
    step_name = "a,b,c,d,e"
    step_state = "0,0,0,0,0"
    response_state = 'success'
    try:
        robot_cmd = int(cmd['robot_state']['process'])
        item = ''
        item = process_parse(robot_cmd)
        if item in PROCESS_ITEM:
            state = get_state(robot_id, item)        
            if not state['flag'] == 0:
                response_state = 'refuse'
            else:
                response_state = 'success'        
            step_name =u','.join(state['state']['step_name'])
            step_state = state_join(state['state']['step_state'])
        elif item == 'troubleshoot':#故障检测
            ult={}
            #---------初始化故障--------------
            state = get_state(robot_id, 'infra_ultra')
            data = state['data']
            step_name = ''
            step_state = ''
            if state['flag'] == 0 and state['flag'] == 1:
                step_name += u'红外初始化,超声初始化,'
                step_state += '0,0,'            
            elif state['flag'] == 3:                
                if len(data)>0:#超声初始化
                    ult[0] = data[0]
                    for i in range(0,13):
                        i=str(i)
                        if not i in ult[0]:
                            step_name += u'初始化超声'+str(i)+':无数据,'                        
                            step_state += str(3)+','
                        elif ult[0][i] == 'N':
                            step_name += u'初始化超声'+str(i)+':'+str(ult[0][i])+','                        
                            step_state += str(3)+','
                if len(data)>1:#红外初始化
                    ult[1] = data[1]
                    for i in range(1,8):
                        if not ('infrared'+str(i)) in ult[1]:
                            step_name += '初始化红外'+str(i)+':无数据,'                        
                            step_state += str(3)+','
                        elif ult[1]['infrared'+str(i)] > 300:
                            step_name += '初始化红外'+str(i)+':'+str(ult[1]['infrared'+str(i)])+','                        
                            step_state += str(3)+','
            #------------------超声测距故障----------------------
            state = get_state(robot_id, 'ultrasonic')
            data = state['data']
            if len(data)>1:
                ult[0] = arr2dic(data[0])
                ult[1] = arr2dic(data[1])
                for i in range(0,13):
                    if not i in ult[1]:
                        step_name += u'远距离超声'+str(i)+':无数据,'                        
                        step_state += str(3)+','
                    elif ult[1][i] == 'N':
                        step_name += u'远距离超声'+str(i)+':'+str(ult[0][i])+','                        
                        step_state += str(3)+','
            if len(data)>3:
                ult[2] = arr2dic(data[2])
                ult[3] = arr2dic(data[3])
                for i in range(0,13):
                    if not i in ult[3]:
                        step_name += u'近距离超声'+str(i)+':无数据,'                        
                        step_state += str(3)+','
                    elif ult[3][i] == 'N':
                        step_name += u'近距离超声'+str(i)+':'+str(ult[2][i])+','                        
                        step_state += str(3)+','
            #------------------红外蔽障故障----------------------
            state = get_state(robot_id, 'infrared')
            data = state['data']
            if len(data)>1:
                ult[0] = data[0]
                ult[1] = data[1]
                for i in range(1,8):
                    if not 'infrared'+str(i) in ult[1]:
                        step_name += '红外蔽障'+str(i)+':无数据,'                        
                        step_state += str(3)+','
                    elif ult[1]['infrared'+str(i)] == 'N':
                        step_name += '红外蔽障'+str(i)+':'+str(ult[0]['infrared'+str(i)])+','                        
                        step_state += str(3)+','            
            #------------------结束故障----------------------
            step_name = step_name[:-1]                       
            step_state = step_state[:-1]
    except:
        response_state = 'success'
        step_name = u"正,在,连,接,..."
        import time   
        i= time.localtime().tm_sec
        if i%2 :
            step_state = "0,0,0,0,0"
        else:
            step_state = "1,1,1,1,1"
    stationstate = 'unselected'
    ResponseInfo = u'{"robot_id":"'+str(robot_id)+\
                   u'","robot_state":{"process":"'+str(robot_cmd)+'","step":"1"},"message":{"process_state":{"process":"'+str(robot_cmd)+\
                   u'","stationstate":"'+str(stationstate)+'","step":{"step_name":"'+step_name+'", "step_state":"'+step_state+\
                   u'" } } },"state":"'+str(response_state)+'"}\r\n'   
    return ResponseInfo

def state_join(state):
    tmp = ''
    for s in state:
        tmp += str(s) + ','
    tmp = tmp[:-1]    
    return tmp

def arr2dic(arr):
    dic = {}
    for a in arr:
        dic[int(a[0])] = a[1]
    return dic

#*****************************************
# function:  get_state
# Date :
# Discription:   获取robot状态
#*****************************************  
def get_state(robot_id, item):    
    RobotDB_Handle = sqlite3.connect("F:\pyserver\Robot.db")
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'SELECT %s FROM RobotCalibration WHERE robot_id = "%s" ' % (item,robot_id)    
    RobotDB_Interface.execute(sql)
    ret = RobotDB_Interface.fetchall()
    RobotDB_Handle.close()
    state = eval(ret[0][0])    
    return state

#处理传入参数
param = parse_qs(os.environ['QUERY_STRING'])
robot_ip = os.environ['REMOTE_ADDR']
print "Content-type:text/html\r\n\r\n"
if ('robot_id' in param) and ('cmd' in param):    
    robot_id = param['robot_id'][0]    
    cmd = param['cmd'][0]
    cmd = eval(cmd)
    ResponseInfo = app(robot_id,cmd,robot_ip)    
    print ResponseInfo


#-*- coding: UTF-8 -*-

import sqlite3
import json
from cgi import parse_qs,escape
import os
import sys
import time
from app_config import *
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(ROBOT_PATH)
from serverTool import *


#*****************************************
# function:  state_join
# Date :
# Discription:
#*****************************************
def state_join(state):
    tmp = ''
    for s in state:
        tmp += str(s) + ','
    tmp = tmp[:-1]
    return tmp

#*****************************************
# function:  get_robot_state
# Date :
# Discription:   获取robot状态
#*****************************************
def get_state(robot_id, item):
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'SELECT %s FROM RobotCalibration WHERE robot_id = "%s" ' % (item,robot_id)
    RobotDB_Interface.execute(sql)
    ret = RobotDB_Interface.fetchall()
    RobotDB_Handle.close()
    state = eval(ret[0][0])
    return state
#*****************************************
# function:  reset_process
# Date :
# Discription:  
#***************************************** 
def reset_process(robot_id,item,data):    
    #重置
    sqlHandle = sqlite3.connect(DATABASE_PATH)
    sqlInterface = sqlHandle.cursor()    
    sql = 'SELECT * FROM RobotCalibration WHERE robot_id = "%s" ' % (robot_id)
    sqlInterface.execute(sql)
    ret = sqlInterface.fetchall()
    if len(ret) == 1 and item != '':        
        try:
            sql = 'update RobotCalibration set %s = "%s" where robot_id = "%s"'        
            data = (item,data,robot_id)
            sql = sql % data
            #print sql
            sqlHandle.execute(sql)
            sqlHandle.commit() 
            sql = 'DELETE FROM robot_list WHERE robot_id = "%s" ' % (robot_id)
            #sql = 'update robot_list set robot_port = "1001" where robot_id = "%s"' % (robot_id)
            sqlHandle.execute(sql)
            sqlHandle.commit()
            sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
            #sql = 'update robot_list set robot_port = "1001" where robot_id = "%s"' % (robot_id)
            sqlHandle.execute(sql)
            sqlHandle.commit()
        except:
            pass
    time.sleep(1)
    sql = 'SELECT %s FROM RobotCalibration WHERE robot_id = "%s" ' % (item,robot_id)
    sqlInterface.execute(sql)
    ret = sqlInterface.fetchall()   
    state = {'flag':0}
    if(len(ret) > 0):
        state = eval(ret[0][0]) 
    sqlHandle.close()
    #获取状态信息
    step = {}
    ResponseInfo = ''
    step_name = "重置"
    step_state = "0"
    response_state = 'success'
    try:        
        if state['flag'] == 0:            
            step_state = "2"
        if state['flag'] == 1:            
            step_state = "3"
        if state['flag'] == 2:            
            step_state = "3"
        if state['flag'] == 3:            
            step_state = "3"
    except:
        pass

    #反馈信息
    global robot_cmd
    ResponseInfo = '{"robot_id":"'+str(robot_id)+'",\
                    "robot_state":{"process":'+str(robot_cmd)+',"step":"1"},\
                    "message":{"process_state":{"process":"'+str(robot_cmd)+'",\
                    "step":{"step_name":"'+step_name+'", "step_state":"'+step_state+'" } } },\
                    "state":"'+str(response_state)+'"}\r\n' 
    return ResponseInfo

#*****************************************
# function: set_process_state
# Date:
# Discription:  
#*****************************************
def set_process_state(flag,data,state):
    st = {}
    st['flag'] = flag
    st['data'] = data
    st['state'] = state
    return str(st)

#-------------------main--------------------
#处理传入参数
param = parse_qs(os.environ['QUERY_STRING'])
robot_ip = os.environ['REMOTE_ADDR']
item = ''
robot_cmd = 1
if ('robot_id' in param) and ('cmd' in param):
    print "Content-type:text/html\r\n\r\n"
    robot_id = param['robot_id'][0]
    cmd = param['cmd'][0]
    cmd = eval(cmd)
    robot_cmd = 0
    if not 'data' in param:
        data = set_process_state(0,[],[])
    else:
        data = param['data'][0]
    robot_cmd = int(cmd['robot_state']['process'])    
    item = process_parse(robot_cmd)
ResponseInfo = reset_process(robot_id,item,data)
print ResponseInfo



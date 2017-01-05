#-*- coding: UTF-8 -*-

import sqlite3
import json
from cgi import parse_qs,escape
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('F:\pyserver')
from serverTool import *
from mylog import*

#*****************************************
# function:  find_roomID
# Date :
# Discription:  
#***************************************** 
def find_roomID(robot_id,roomID,maxroom):
    if roomID[1]=='x':
        try:
            for i in range(1,(maxroom+1)):            
                sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
                sqlInterface = sqlHandle.cursor()
                findroom=roomID[0]+str(i)
                sql = 'SELECT * FROM robot_room WHERE roomID = "%s" ' % (findroom)
                sqlInterface.execute(sql)
                ret = sqlInterface.fetchall()
                sqlHandle.close()
                if len(ret) == 0:                    
                    return int(findroom[1])
                elif len(ret) == 1:                    
                    if ret[0][1]==robot_id:                        
                        return int(findroom[1])
            return -1
        except:
            logger.error('open table:robot_room error')
            return -2
    if int(roomID[1])>=1 and int(roomID[1])<=maxroom:
        try:
            sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
            sqlInterface = sqlHandle.cursor()    
            sql = 'SELECT * FROM robot_room WHERE roomID = "%s" ' % (roomID)
            sqlInterface.execute(sql)
            ret = sqlInterface.fetchall()
            sqlHandle.close()
            if len(ret) == 0:                
                return int(roomID[1])
            elif len(ret) == 1:
                    #print 'z11=',ret[0][1]                    
                    if ret[0][1]==robot_id:
                        #print 'go'
                        return int(roomID[1])
                    #print 'zz'
                    return -1
        except:
            #print 'wer'
            logger.error('open table:robot_room error')
            return -2
  
    
#*****************************************
# function:  get_roomID
# Date :
# Discription:  
#***************************************** 
def get_roomID(robot_id,process,roomID,maxroom): 
    sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
    sqlInterface = sqlHandle.cursor()    
    sql = 'SELECT * FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
    sqlInterface.execute(sql)
    ret = sqlInterface.fetchall()    
    '''
    ####zc modify 后续对同一数据库开启不同句柄的优化处理
    
    '''
    ResponseInfo = ''
    step_name = "a"
    step_state = "1"
    response_state = 'success'
    #1--- 当前机器人 已经选择了 roomID ---
    if len(ret) == 1 and process != '':        
        try:
            #print 'wert'
            List_sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
            List_sqlInterface = List_sqlHandle.cursor()    
            sql = 'SELECT * FROM robot_list WHERE robot_id = "%s" ' % (robot_id)
            List_sqlInterface.execute(sql)
            ret = List_sqlInterface.fetchall()
            List_sqlHandle.close()
            if len(ret) == 0: #--- 该机器人 流程未运行 ---
                if roomID[1]=='x':                       
                    sql = 'SELECT roomID FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
                    sqlInterface.execute(sql)
                    ret = sqlInterface.fetchall()                                        
                    if len(ret) == 1 and ret[0][0][0]==roomID[0]:                        
                        #print 'roomID has acquired'                        
                        step_name=u'工位 已经选择为 %s'%(ret[0][0])
                        step_state="2"
                    elif len(ret) == 1 and ret[0][0][0]!=roomID[0]:  
                        sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id) 
                        sqlHandle.execute(sql)
                        sqlHandle.commit()                            
                        time.sleep(0.5)
                        step_name=u'上一流程工位已经删除，请选择新工位'
                        step_state="2"                        
                elif int(roomID[1])>=1 and int(roomID[1])<=maxroom:
                    try:                        
                        state=find_roomID(robot_id,roomID,maxroom)
                        #print 'z2=',state
                        
                        if state== int(roomID[1]):                            
                            sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id) 
                            sqlHandle.execute(sql)
                            sqlHandle.commit()                            
                            time.sleep(1)                            
                            sql = 'INSERT INTO robot_room(roomID,robot_id,process)values ("%s", "%s", "%s")'
                            data = (roomID,robot_id,process)
                            sql = sql % data
                            #print sql                            
                            sqlInterface.execute(sql)
                            sqlHandle.commit()                                                        
                            step_name= u'工位选择为：%s'%(roomID)
                            step_state="2"
                        elif state==(-1):                            
                            #print 'this roomID has used,please change roomID'
                            step_name= u'此工位:%s 已经被占用，请更换工位号，'%(roomID)
                            step_state="3"
                        elif state==(-2):
                            step_name= '1open table:robot_room error'
                            step_state="3"
                            #print 'open table:robot_room error'
                            pass 
                    except:
                        step_name= '2open table:robot_room error'
                        step_state="3"
                        pass
            else:
                step_name = "the robot has running"
                step_state = "1"
                #print 'the robot has running, please don`t change roomID'
                logger.info('the robot has running, please don,t change roomID')
        except:
            pass
    #2--- 当前机器人 没有选择 roomID --
    elif len(ret) == 0 and process != '':        
        if roomID[1]=='x':
            try:                
                state=find_roomID(robot_id,roomID,maxroom)                
                if state>=1 and state<=maxroom:                     
                    sql = 'INSERT INTO robot_room(roomID,robot_id,process)values ("%s", "%s", "%s")'
                    get_roomID=roomID[0]+str(state)                    
                    data = (get_roomID,robot_id,process)
                    sql = sql % data
                    #print sql                    
                    sqlInterface.execute(sql)                    
                    sqlHandle.commit()                                       
                    step_name= u'工位选择为：%s%d'%(roomID[0],(state))
                    step_state="2"
                elif state==(-1):
                    #print 'all room have used,please wait'
                    step_name=u'所有工位已经被占用，请等待 '
                    step_state="3"
                elif state==(-2):
                    step_name= '3open table:robot_room error'
                    step_state="3"
                    #print 'open table:robot_room error'
                    pass
                    
            except:
                step_name= '4open table:robot_room error'
                step_state="3"
                pass
        elif int(roomID[1])>=1 and int(roomID[1])<=maxroom:
            try:                
                state=find_roomID(robot_id,roomID,maxroom)
                #print 'w1',state,'w'
                if state== int(roomID[1]):
                    sql = 'INSERT INTO robot_room(roomID,robot_id,process)values ("%s", "%s", "%s")'                    
                    data = (roomID,robot_id,process)
                    sql = sql % data
                    #print sql
                    sqlInterface.execute(sql)                    
                    sqlHandle.commit()                                        
                    step_name=u'工位选择为 %s'%roomID
                    step_state="2"
                elif state==(-1):                    
                    #print 'this roomID has used,please change roomID'
                    step_name=u'此工位：%s 已经被占用，请更换工位号 '%(roomID)                    
                    step_state="3"
                elif state==(-2):
                    step_name= '5open table:robot_room error'
                    step_state="3"
                    #print 'open table:robot_room error'
                    pass
                                    
            except:
                step_name= '6open table:robot_room error'
                step_state="3"
                pass
            
    sqlHandle.close()        
    response_state  = 'success'
    stationstate = 'selected'
    #反馈信息
    global robot_cmd
    ResponseInfo = '{"robot_id":"'+str(robot_id)+'",\
"robot_state":{"process":'+str(robot_cmd)+',"step":"1"},\
"message":{"process_state":{"process":"'+str(robot_cmd)+'","stationstate":"'+str(stationstate)+'",\
"step":{"step_name":"'+step_name+'", "step_state":"'+step_state+'" } } },\
"state":"'+str(response_state)+'"}\r\n'
    return ResponseInfo

#*****************************************
# function:  remove_roomID
# Date :
# Discription:  
#***************************************** 
def remove_roomID(robot_id): 
    sqlHandle = sqlite3.connect("F:\pyserver\Robot.db")
    sqlInterface = sqlHandle.cursor()    
    sql = 'SELECT * FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
    sqlInterface.execute(sql)
    ret = sqlInterface.fetchall()    
    
    ResponseInfo = ''
    step_name = "a"
    step_state = "1"
    response_state = 'success'

    if len(ret) >= 1 :        
        try:
            sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id) 
            sqlHandle.execute(sql)
            sqlHandle.commit()                            
            time.sleep(0.5)
        except:
            pass
    step_name = u"取消工位成功"
    step_state = "2"    
    sqlHandle.close()
    #反馈信息
    global robot_cmd
    stationstate = 'selected'
    ResponseInfo = '{"robot_id":"'+str(robot_id)+'",\
"robot_state":{"process":'+str(robot_cmd)+',"step":"1"},\
"message":{"process_state":{"process":"'+str(robot_cmd)+'","stationstate":"'+str(stationstate)+'",\
"step":{"step_name":"'+step_name+'", "step_state":"'+step_state+'" } } },\
"state":"'+str(response_state)+'"}\r\n'
    return ResponseInfo
               
            

#-------------------main--------------------
#处理传入参数
html_str = "Content-type:text/html\r\n\r\n"
param = parse_qs(os.environ['QUERY_STRING'])
robot_ip = os.environ['REMOTE_ADDR']
item = ''
robot_cmd = 1
if ('robot_id' in param) and ('cmd' in param):    
    robot_id = param['robot_id'][0]
    cmd = param['cmd'][0]
    cmd = eval(cmd)
    robot_cmd = 0
    
    robot_cmd = int(cmd['robot_state']['process'])
    request=cmd['robot_request']['request']
    if request=='set_station' or request=='get_station':
        roomID=cmd['robot_request']['station'] #C3 Cx
        if roomID[0]=='B':
            maxroom=2            
        process = process_parse(robot_cmd)
        #print robot_id,process,roomID,maxroom
        ResponseInfo = get_roomID(robot_id,process,roomID,maxroom)
        html_str += str(ResponseInfo)+'\r\n'
    elif request=='set_station_right' or request=='get_station_right' or request=='set_station_left' or request=='get_station_left':
        if request=='set_station_right' or request=='get_station_right' :
            roomID='R'+cmd['robot_request']['station'][1]
        elif request=='set_station_left' or request=='get_station_left' :
            roomID='L'+cmd['robot_request']['station'][1]        
        maxroom=6            
        process = process_parse(robot_cmd)        
        ResponseInfo = get_roomID(robot_id,process,roomID,maxroom)
        html_str += str(ResponseInfo)+'\r\n'
    elif request=='remove_station' or request=='remove_station_left' or request=='remove_station_right':
        ResponseInfo = remove_roomID(robot_id)
        html_str += ResponseInfo+'\r\n'
        
print html_str






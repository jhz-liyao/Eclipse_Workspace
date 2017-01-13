# -*- coding: utf-8 -*-
from protocol import *
from formula  import *
import sqlite3
from sys_env import *
from time import * 
from app_config import *
#*****************************************
# function:  creat_robot_state
# Date :
# Discription:   构建 robot状态表
#*****************************************  
def creat_robot_state(robot):    
    move = str(set_process_state(0,[],{}))
    odometer = str(set_process_state(0,[],{}))
    navigation = str(set_process_state(0,[],{}))
    infra_ultra = str(set_process_state(0,[],{}))
    wheelspace = str(set_process_state(0,[],{}))
    camera = str(set_process_state(0,[],{}))
    infrared = str(set_process_state(0,[],{}))
    ultrasonic = str(set_process_state(0,[],{}))
    charging = str(set_process_state(0,[],{}))
    allstatus = '0'
    move_check = str(set_process_state(0,[],{}))
    wheelspace_check = str(set_process_state(0,[],{}))
    #插入数据
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'SELECT * FROM RobotCalibration WHERE robot_id = "%s" ' % (robot.robot_id)    
    RobotDB_Interface.execute(sql)
    ret = RobotDB_Interface.fetchall()
    #print ret
    if len(ret)==0:
        
        sql = 'INSERT INTO RobotCalibration(robot_id, move, odometer,infra_ultra,navigation, wheelspace,\
camera, infrared, ultrasonic,charging,allstatus,move_check,wheelspace_check)\
values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        data = ( robot.robot_id, move, odometer,infra_ultra, navigation, wheelspace,\
                 camera, infrared, ultrasonic,charging,allstatus,move_check,wheelspace_check)
        sql = sql % data
        print '++++++++INSERT ROBOT+++++++++'
        RobotDB_Handle.execute(sql)
        RobotDB_Handle.commit()    
    RobotDB_Handle.close()
        
def set_process_state(flag,data,state):
    st = {}
    st['flag'] = flag
    st['data'] = data
    st['state'] = state
    return str(st)
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
    if len(ret) == 1:
        sql = 'update RobotCalibration set %s = "%s" where robot_id = "%s"'
        data = (item,data,robot_id)
        sql = sql % data
        sqlHandle.execute(sql)
        sqlHandle.commit()
    sqlHandle.close()
    return 'ok'
#*****************************************
# function:  update_process_state
# Date :
# Discription:   更新process状态
#*****************************************
def update_process_state(robot,process,state):
    state = str(state)
    #更新数据
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'UPDATE calibration_evn SET  state = "%s" WHERE name = "%s"'
    data = (state,process)
    sql = sql % data
    #print sql
    RobotDB_Handle.execute(sql)
    RobotDB_Handle.commit()
    RobotDB_Handle.close()

#*****************************************
# function:  update_robot_state
# Date :
# Discription:   更新robot状态
#*****************************************  
def update_robot_state(robot, item, flag, data,state):
    state_last = get_robot_state(robot, item)
    if data =="":
        data = state_last['data']
    if flag == "":
        flag = state_last['flag']
    if state == "":
        state = state_last['state']
    st = set_process_state(flag,data,state)
    #更新数据             
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'UPDATE RobotCalibration SET  %s = "%s" WHERE robot_id = "%s"'
    data = (item , st, robot.robot_id)
    sql = sql % data
    #print sql
    RobotDB_Handle.execute(sql)
    RobotDB_Handle.commit()
    RobotDB_Handle.close()

#*****************************************
# function:  get_process_state
# Date :
# Discription:   获取process状态
#*****************************************
def get_process_state(robot,process):
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'SELECT process FROM calibration_evn WHERE robotID = "%s" ' % (robot.robot_id)
    RobotDB_Interface.execute(sql)
    ret = RobotDB_Interface.fetchall()
    if len(ret)==0:        
        sql = 'INSERT INTO calibration_evn(process,group_type,robotID)values ("%s", "%s", "%s")'
        data = (process,'process',robot.robot_id)
        sql = sql % data
        print sql
        RobotDB_Handle.execute(sql)
        RobotDB_Handle.commit()
        RobotDB_Handle.close()        
    else:        
        sql = 'UPDATE calibration_evn SET  process = "%s" WHERE robotID = "%s"'
        data = (process ,robot.robot_id)
        sql = sql % data
        #print sql
        RobotDB_Handle.execute(sql)
        RobotDB_Handle.commit()
        RobotDB_Handle.close()
    return process
#*****************************************
# function:  get_robot_state
# Date :
# Discription:   获取robot状态
#*****************************************  
def get_robot_state(robot, item):    
    RobotDB_Handle = sqlite3.connect(DATABASE_PATH)
    RobotDB_Interface = RobotDB_Handle.cursor()
    sql = 'SELECT %s FROM RobotCalibration WHERE robot_id = "%s" ' % (item,robot.robot_id)
    RobotDB_Interface.execute(sql)
    ret = RobotDB_Interface.fetchall()
    RobotDB_Handle.close()
    #print ret[0][0]
    try:
        state = eval(ret[0][0])
    except:
        state = eval(set_process_state(0,[],{}))
    return state


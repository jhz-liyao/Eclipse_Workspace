# -*- coding: UTF-8 -*-
from serverTool import *
import sqlite3
import os
from myThread import *
from sys_env import *
from time import *
from protocol import *
from process import *
from rotaryinit import *
from app_config import *

sqlHandle = sqlite3.connect(DATABASE_PATH)
sqlInterface = sqlHandle.cursor()
robot_list = {}

def robot_task(robot):
    get_robot_connection_state(robot)
    creat_robot_state(robot)    
    while 1:
        print '*robot_id:' + str(robot.robot_id)+'process:' + str(robot.cmd)        
        item = ''
        item = process_parse(robot.cmd)
        if item != '' and robot.cmd != 0:            
            excute_process(robot, item)
            robot.cmd = 0
            sqlHandle = sqlite3.connect(DATABASE_PATH)
            sqlInterface = sqlHandle.cursor()
            sql = 'DELETE FROM robot_list WHERE robot_id = "%s" ' % (robot.robot_id) 
            sqlHandle.execute(sql)
            sqlHandle.commit()
            sqlHandle.close()        
        if 1:            
            break
    robot.connectTCP.connectTCP.close()    
    print robot_list
    

    
def listener():
    global Occupy_wheelspace_Road_Robot_List
    global Occupy_infra_ultra_Road_Robot_List
    global Occupy_CL_Road_Robot_List
    global Occupy_CR_Road_Robot_List
    sqlInterface.execute("select * from robot_list")
    robot_state_list = sqlInterface.fetchall()
    print u'-------listen Robot--------------'
    for robot in robot_state_list:
        robot_id =robot[1]
        robot_ip =robot[2]
        robot_port =robot[3]
        robot_cmd =robot[4]        
        print 'START:',robot_id
        if not robot_id in robot_list:
            try:                
                robot_list[robot_id] = Robots(robot_id, robot_ip, robot_port)  #构建robot实例            
                robot_list[robot_id].mainthread = Robot_thread(robot_id, robot_list[robot_id], robot_task,robot_id)  #开启robot子线程
                robot_list[robot_id].mainthread.start()
                
            except:
                if robot_id in robot_list:
                    del robot_list[robot_id]
        if robot_id in robot_list:            
            robot_list[robot_id].cmd = eval(robot_cmd)
        print 'END'
    for robot_id in robot_list.keys():                   
        threadstate= robot_list[robot_id].mainthread.isAlive()        
        if threadstate !=True:
            if robot_id in Occupy_wheelspace_Road_Robot_List:
                del Occupy_wheelspace_Robot_List[0]
            #if robot_id in Occupy_infra_ultra_Road_Robot_List:
                #del Occupy_infra_ultra_Road_Robot_List[0]
            if robot_id in Occupy_CL_Road_Robot_List:
                del Occupy_CL_Road_Robot_List[0]
            if robot_id in Occupy_CR_Road_Robot_List:
                del Occupy_CR_Road_Robot_List[0]
            del robot_list[robot_id] 
            print u'线程已经关闭'
            print ' del robot_list[%s]'%(robot_id)
        

sqlInterface.execute("select * from robot_list")
robot_list_info = sqlInterface.fetchall()
print  '--listener ready start,remove all robot_list info--' + ROBOT_PATH
for robot in robot_list_info:
    robot_id =robot[1]
    sql = 'DELETE FROM robot_list WHERE robot_id = "%s" ' % (robot_id) 
    sqlHandle.execute(sql)
    sqlHandle.commit()
    
'''
####zc modify 无用操作

sqlInterface.execute("select * from calibration_evn")
robot_list_info = sqlInterface.fetchall()
print  '--listener ready start,remove all calibration_evn info--'
for robot in robot_list_info:
    _id =robot[0]
    sql = 'DELETE FROM calibration_evn WHERE id = "%s" ' % (_id) 
    sqlHandle.execute(sql)
    sqlHandle.commit()
'''
        
#rotary_init('')
while 1:
    listener()
    print 'main run' 
    sleep(0.5)

sqlHandle.close()
for r_id in robot_arr:
    robot_arr[r_id].thread.join()

# -*- coding: utf-8 -*-
from protocol import *
from formula  import *
import sqlite3
from sys_env import *
from time import *
from state import *
from readconf import *
from app_config import *
Occupy_wheelspace_Road_Robot_List = []
Occupy_infra_ultra_Road_Robot_List = []
Occupy_CL_Road_Robot_List = []
Occupy_CR_Road_Robot_List = []
Occupy_L0_Robot = ""
Occupy_R0_Robot = ""
#*****************************************
# function:  process
# Date :
# Discription:   执行各个标定过程
#*****************************************  
def excute_process(robot, item):
    print item
    #liyao
    #STEP0
    #+++++++++++++++camera_first+++++++++++++++++++++++++++++++++++++++++
    if item == 'camera_first':
        excute_process_calibration(excute_camera_first_calibration,robot, item,'')
    #STEP1
    #+++++++++++++++move+++++++++++++++++++++++++++++++++++++++++
    if item == 'move':
        excute_process_calibration(excute_move_calibration,robot, item,'')
    #STEP2
    #+++++++++++++++odometer+++++++++++++++++++++++++++++++++++++++++
    if item == 'odometer':
        excute_process_calibration(excute_odometer_calibration,robot, item,'')
    #STEP3
    #+++++++++++++++wheelspace +++++++++++++++++++++++++++++++++++++++++
    if item == 'wheelspace':
        excute_process_calibration(excute_wheelspace_calibration,robot, item,'')
    #STEP4
    #+++++++++++++++infra_ultra +++++++++++++++++++++++++++++++++++++++++
    if item == 'infra_ultra':
        excute_process_calibration(excute_infra_ultra_calibration,robot, item,'')        
    #STEP5
    #+++++++++++++++camera +++++++++++++++++++++++++++++++++++++++++
    if item == 'camera':
        excute_process_calibration(excute_camera_calibration,robot, item,'')
    #STEP11
    #+++++++++++++++move_check +++++++++++++++++++++++++++++++++++++++++
    if item == 'move_check':
        excute_process_calibration(excute_move_check_calibration,robot, item,'')    #STEP5
    #+++++++++++++++wheelspace_check +++++++++++++++++++++++++++++++++++++++++
    if item == 'wheelspace_check':
        excute_process_calibration(excute_wheelspace_check_calibration,robot, item,'')   
            
def excute_process_calibration(_fun, robot, item, arg):
    st = ''
    st = get_robot_state(robot, item)
    sleep(2)  #--- 可删除
    if st['flag']==0:        
        process_state = get_process_state(robot,item)
        print robot.robot_id,'run',process_state
        switch_obstacle_status(robot,0,'')
        open_ultrasonic_feedback(robot,0,[0])
        get_infrared_statusfeed(robot,0,'')
        open_navigation_switch(robot,"stop",'')        
        _fun(robot, item,'')
        state = {}              
        switch_obstacle_status(robot,0,'')
        open_ultrasonic_feedback(robot,0,[0])
        get_infrared_statusfeed(robot,0,'')
        open_navigation_switch(robot,"stop",'')
            
#*****************************************
# function:  excute_move_calibration
# Date :
# Discription:   执行行走控制标定过程
#*****************************************  
def excute_move_calibration(robot,item,arg):
    flag = 1
    data={}
    dat = [7.03546,20,1,1,0,0,0,0,0,0]
    set_motorcomp(robot,2,dat)
    sleep(3)
    state = {}
    state['step_name'] = [u"获取相机数据",u"行走5米",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    wing_move_angle(robot,"move",30)
    data[0] = [1,1,1,1,1,0,0,0,0,0]    
    set_motorcomp(robot, 1, data[0])    
    sleep(2)
    flagr,moveinfo=read_configfile('move')
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    else:
        move_d1 =  moveinfo[0] 
        move_d2 =  moveinfo[1]
        move_wheelbase =  moveinfo[2]
        move_d3 =  moveinfo[3] 
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------    
    print '\n','step1' 
    open_navigation_switch(robot,"stop",'')
    set_navigation(robot, 0, 0, 0)     
    sleep(3)    
    flagca,y_start=get_camera_info('00263780','pos','192.168.2.110')                        ####zc comment: ID，确定， IP:固定
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1    
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)    
    #2    
    #-----------行走5米-----------
    print '\n','step2'
    wheel_move_distance(robot,"front_distance",move_d1)
    sleep(27)
    flag = 1     
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3    
    #-----------获取相机数据-----------
    print '\n','step3'
    flagca,y_end=get_camera_info('00399800','pos','192.168.2.110')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,3,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0    
    sleep(2)
    flag = 1    
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)    
    #4
    #-----------计算下载数据-----------
    print '\n','step4'

    ####zc comment：仅作参考，不影响流程    
    #--- 航位 仅作显示 参考---
    odoflag,odometer_y =open_navigation_switch(robot,"start",'')
    print 'odometer_y=',odometer_y
    open_navigation_switch(robot,"stop",'')
    
    delta = float(y_end-y_start)
    print 'delta=',delta
    data[1]=delta
    if abs(delta) >15 and abs(delta) <250:
        [k,th,R] = calc_motor_control_compensation(delta,move_d1,move_wheelbase)
        print k
        if delta > 0:
            data[0] = [k,1,1,1,1,0,0,0,0,0]
        else:
            data[0] = [1,k,1,1,1,0,0,0,0,0]
        set_motorcomp(robot, 1, data[0])
    
    ####zc add 增加超过250的判断  
    
    flag = 1
    sleep(2)
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)    
    #5-1
    #-----------下一站-----------
    print '\n','step5'
    wheel_move_angle(robot,"left_angle",90)                     
    sleep(3)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-2
    #-----------下一站-----------
    wheel_move_distance(robot,"front_distance",move_d2 )            
    sleep(10)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-3
    #-----------下一站-----------
    wheel_move_angle(robot,"left_angle",90)            
    sleep(4)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-4
    #-----------下一站-----------
    wheel_move_distance(robot,"back_distance",move_d3)            
    sleep(5)
    wing_move_angle(robot,"move",0)
    flag = 2
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---move_calibration over---'

#*****************************************
# function:  excute_odometer_calibration
# Date :
# Discription:   执行行走航位标定过程
#*****************************************  
def excute_odometer_calibration(robot, item,arg):
    flag = 1
    data={}
    dat = [7.03546,20,1,1,0,0,0,0,0,0]
    set_motorcomp(robot,2,dat)
    sleep(3)
    state = {}
    state['step_name'] = [u"获取相机数据",u"行走5米",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    data[0] = [1,1,1,1,1,0,0,0,0,0]
    set_motorcomp(robot, 3, data[0])    
    sleep(2)
    flagr,odometerinfo=read_configfile('odometer')
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    else:
        odometer_d1 =  odometerinfo[0] 
        odometer_wheelbase =  odometerinfo[1] 
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    #wing_move_angle(robot,"move",30)
    sleep(2)
    open_navigation_switch(robot,"stop",'')
    set_navigation(robot, 0, 0, 0)
    sleep(2)    
    flagca,y_start=get_camera_info('00366817','pos','192.168.3.111')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1    
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #2
    #-----------行走5米-----------
    print '\n','step2'    
    wheel_move_distance(robot,"front_distance",odometer_d1)            
    sleep(30)
    flag = 1    
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    sleep(2)
    flagca,y_end=get_camera_info('00408370','pos','192.168.3.111')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,3,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1    
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------计算下载数据-----------
    print '\n','step4'
    odoflag,odometer_y =open_navigation_switch(robot,"start",'')
    if odoflag==-1:
        flag=3
        wing_move_angle(robot,"move",80)
        open_navigation_switch(robot,"stop",'')
        sleep(2)
        state['step_state'] = [2,2,2,3,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    open_navigation_switch(robot,"stop",'')
    delta = float(y_end-y_start)    
    ododelta=odometer_y-delta    
    data[1]= delta  ;#1--- 行走 偏差
    data[2]= odometer_y ;#2--- 航位 值
    data[3]= ododelta  ;#3--- 航位 偏差
    print '1delta=',delta
    print '2odometer_y =',odometer_y
    print '3ododelta=',ododelta
    
    #--- 行走 偏差值 大于 300 就失败（代表 行走控制 有问题！）    
    if abs(delta) >100:                                        #300--------3000改回来---------------------------------------------------------------------------------
        flag=3
        wing_move_angle(robot,"move",80)
        open_navigation_switch(robot,"stop",'')
        sleep(2)
        wheel_move_angle(robot,"right_angle",90)   #--- 结合 相机能精确运动到 维修区                  
        sleep(3)
        wheel_move_distance(robot,"front_distance",1500 )            
        sleep(10)        
        state['step_state'] = [2,2,2,3,0]
        update_robot_state(robot, item, flag, data,state)
        return 0    
    if abs(ododelta)>50:#------------------------------------------------------------------------------------15
        [k,th,R] = calc_DeadReckoning_compensation(ododelta,odometer_d1,odometer_wheelbase)
        print k
        if ododelta > 0:
            data[0] = [k,1,1,1,1,0,0,0,0,0]
        else:
            data[0] = [1,k,1,1,1,0,0,0,0,0]
        #set_motorcomp(robot, 3, data[0])
    sleep(2)    
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'    
    wing_move_angle(robot,"move",0)  
    sleep(2)
    flag = 2
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---odometer_calibration over---'
    
#*****************************************
# function:  excute_wheelspace_calibration
# Date :
# Discription:   执行 轮间距标定 过程
#*****************************************  
def excute_wheelspace_calibration(robot, item, arg):    
    global Occupy_wheelspace_Road_Robot_List
    global Occupy_infra_ultra_Road_Robot_List
    global Occupy_L0_Robot
    global Occupy_R0_Robot
    flag = 1
    data={}
    dat = [7.03546,20,1,1,0,0,0,0,0,0]
    set_motorcomp(robot,2,dat)
    sleep(3)
    state = {}
    state['step_name'] = [u"获取工位号/运动到标定处",u"获取相机数据",u"转动10圈",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    state['step_state'] = [1,0,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    sleep(0.5)
    #1-1
    #-----------获取流程工位号-----------
    print '\n','step1-1'
    #wing_move_angle(robot,"move",30)
    sleep(3)
    flagg,roomID=get_roomID(robot, item)
    if flagg==3 or flagg==(-1):
        flag=3 
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    state['step_name'][0]=u"获取工位号:%s 运动到标定处"%(roomID)
    flagr,wheelspaceinfo=read_configfile('wheelspace')
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    else:
        wheelspace_n =  wheelspaceinfo[0] 
        wheelspace_base =  wheelspaceinfo[1]
        wheelspace_H = wheelspaceinfo[2]
        wheelspace_L = wheelspaceinfo[3]
        wheelspace_theta = wheelspaceinfo[4]
    data[0] = [wheelspace_base ,0,0,0,0,0,0,0,0,0]
    set_motorcomp(robot, 4, data[0])
    sleep(2)
    data[2] = roomID
    state['step_state'] = [1,0,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1-2
    #-----------运动到轮间距标定处-----------
    print '\n','step1-2'    
    flagca,info_start=get_camera_info('00408370','pos_angle','192.168.3.111') #---------------------------------------------------ok   
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0    
    #--- 通过相机反馈的(坐标+角度)调整机器人位置
    start_x=info_start[0]
    start_y=info_start[1]
    start_angle=info_start[2]
    if start_angle>0:
        angle_11=360-start_angle
        wheel_move_angle(robot,"right_angle",angle_11)
    else:
        angle_11=360+start_angle
        wheel_move_angle(robot,"left_angle", angle_11)
    time_angle=angle_11/22.5+1
    if time_angle<3:
        time_angle=3
    sleep(time_angle)
    #wheelspace抢占跑道
    if int(roomID[1])==1:
        if not (robot.robot_id in Occupy_wheelspace_Road_Robot_List):
             Occupy_wheelspace_Road_Robot_List.append(robot.robot_id)#加入抢占左侧跑道队列
            #++++++滤波，等待，核实，决策+++++
        sleep(3)
        if robot.robot_id in Occupy_wheelspace_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_wheelspace_Road_Robot_List[0] == robot.robot_id:      
                    break #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [3,0,0,0,0,0]
                    update_robot_state(robot, item, flag, data,state)
                    return 0    
    wheel_d1=1270-start_x
    wheel_move_distance(robot,"front_distance",wheel_d1)            
    sleep(10)
    if int(roomID[1])==1:        
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
        wheel_d2=2430-start_y  
        wheel_move_distance(robot,"front_distance",wheel_d2)
        sleep(18)
        #释放wheelspace跑道
        if robot.robot_id in Occupy_wheelspace_Road_Robot_List:
            del Occupy_wheelspace_Road_Robot_List[0]
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
    else:
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
        wheel_d3=1430+start_y
        wheel_move_distance(robot,"front_distance",wheel_d3)
        sleep(18)
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
    flag = 1    
    state['step_state'] = [2,1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)    
    #2
    #-----------获取相机数据-----------
    print '\n','step2'
    if int(roomID[1])==1:   #--- 改为 轮间距相机对应ID----------------------------------------------------------------------------ok
        cameraID='00289713'
    elif int(roomID[1])==2:
        cameraID='00270925'     #### zc comment 待确认 ---------------------------------------------------------------------------ok
    flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.4.112')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    start_x=info_start[0]
    start_y=info_start[1]
    start_angle=info_start[2]    
    if start_angle>0:
        angle_12 = 270-start_angle
        wheel_move_angle(robot,"right_angle",angle_12)
        sleep(6)
        wheel_d2=start_y
        if wheel_d2>10:
            wheel_move_distance(robot,"back_distance",wheel_d2)
        elif wheel_d2<-10:
            wheel_move_distance(robot,"front_distance",-wheel_d2)
        sleep(4)
        wheel_move_angle(robot,"right_angle",90)    
    else:
        angle_13 = 270+start_angle
        wheel_move_angle(robot,"left_angle",angle_13)
        sleep(6)
        wheel_d2=start_y
        if wheel_d2>10:
            wheel_move_distance(robot,"front_distance",wheel_d2)
        elif wheel_d2<-10:
            wheel_move_distance(robot,"back_distance",-wheel_d2)
        sleep(4)
        wheel_move_angle(robot,"left_angle",90)
    sleep(4)
    if start_x>10:
        wheel_move_distance(robot,"back_distance",start_x)
    elif start_x<-10:
        wheel_move_distance(robot,"front_distance",-start_x)
    sleep(4)
    
    if int(roomID[1])==1:   #--- 改为 轮间距相机对应ID----------------------------------------------------------------------------ok
        cameraID='00289713'
    elif int(roomID[1])==2:
        cameraID='00270925'     #### zc comment 待确认 ---------------------------------------------------------------------------ok
    flagca,theta_start=get_camera_info(cameraID,'angle','192.168.4.112')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    print 'camera con'    
    flag = 1    
    state['step_state'] = [2,2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------转动10圈-----------
    print '\n','step3'    
    wheel_move_angle(robot,"right_angle",wheelspace_n*360)           
    sleep(90)
    #wheel_move_angle(robot,"right_angle",360)
    #sleep(9)
    flag = 1    
    state['step_state'] = [2,2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------获取相机数据-----------
    print '\n','step4'
    flagca,theta_end=get_camera_info(cameraID,'angle','192.168.4.112')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,3,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(1)
    flag = 1    
    state['step_state'] = [2,2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #5
    #-----------计算下载数据-----------
    print '\n','step5'
    wheelbaseH=wheelspace_base + wheelspace_H
    wheelbaseL=wheelspace_base - wheelspace_L
    R_angle = float(theta_end+wheelspace_n*360-theta_start)
    V_angle = wheelspace_n*360
    delta_angle=R_angle -V_angle
    data[1]= delta_angle
    print 'delta_angle=',delta_angle
    if abs(delta_angle)>10:
        k = V_angle/R_angle
        wheelbase=wheelspace_base*k
        if wheelbase >wheelbaseH or wheelbase <wheelbaseL :
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,2,3,0]
            update_robot_state(robot, item, flag, data,state)
            return 0        
        data[0] = [wheelspace_base*k,0,0,0,0,0,0,0,0,0]
        set_motorcomp(robot, 4, data[0])
        sleep(2)
    flag = 1
    state['step_state'] = [2,2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
   
    #7
    #-----------下一站-----------
    print '\n','step7'    
    
    if delta_angle>0:
        wheel_move_angle(robot,"left_angle",delta_angle+wheelspace_theta)
    else:
        wheel_move_angle(robot,"right_angle",-delta_angle+wheelspace_theta)
    sleep(11)
    '''
    if int(roomID[1])==1:
       wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
    else:
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
     '''   
    #--- 通过相机反馈的(坐标+角度)调整机器人位置
    flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.4.112')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,2,2,3]
        update_robot_state(robot, item, flag, data,state)
        return 0 
    start_x=info_start[0]
    start_y=info_start[1]
    start_angle=info_start[2]

     #-----------抢占跑道-----------
    #infra_ultra抢占队列
    if not (robot.robot_id in Occupy_infra_ultra_Road_Robot_List):
        Occupy_infra_ultra_Road_Robot_List.append(robot.robot_id)#加入抢占左侧跑道队列
        #++++++滤波，等待，核实，决策+++++
    sleep(3)
    if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
        occ=0
        while 1: #循环等待抢占结果
            if Occupy_infra_ultra_Road_Robot_List[0] == robot.robot_id:      
                break #直到抢占列表轮转到当前小胖跳槽循环
            sleep(2)
            occ += 1
            if occ>300:
                print '等待抢占超时'
                wing_move_angle(robot,"move",80)
                flag=3
                state['step_state'] = [2,2,2,2,2,3]
                update_robot_state(robot, item, flag, data,state)
                return 0         
    #wheelspace抢占队列
    if int(roomID[1])==2:
        if not (robot.robot_id in Occupy_wheelspace_Road_Robot_List):
            Occupy_wheelspace_Road_Robot_List.append(robot.robot_id)#加入抢占左侧跑道队列
            #++++++滤波，等待，核实，决策+++++
        sleep(2)
        if robot.robot_id in Occupy_wheelspace_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_wheelspace_Road_Robot_List[0] == robot.robot_id:      
                    break #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [2,2,2,2,2,3]
                    update_robot_state(robot, item, flag, data,state)
                    return 0         
    ####zc comment 判断 start_angle取值范围，验证轮间距补偿结果
    if int(roomID[1])==1:        
        wheel_move_angle(robot,"left_angle",92.5+start_angle)        
        sleep(3)
        wheel_d1=1540+start_y
        wheel_move_distance(robot,"front_distance",wheel_d1)            
        sleep(15)
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)        
    else:
        wheel_move_angle(robot,"right_angle",90-start_angle)            
        sleep(3)
        wheel_d1=2410-start_y
        wheel_move_distance(robot,"front_distance",wheel_d1)            
        sleep(15)
        #释放wheelspace跑道
        if robot.robot_id in Occupy_wheelspace_Road_Robot_List:
            del Occupy_wheelspace_Road_Robot_List[0]
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
        
    
    
    #-------------让出工位---------------------------------------
    sqlHandle = sqlite3.connect(DATABASE_PATH)
    sqlInterface = sqlHandle.cursor()
    #sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
    sql = 'update robot_room set roomID = "%s" where robot_id = "%s"' % ('X'+roomID[1], robot.robot_id)
    sqlHandle.execute(sql)
    sqlHandle.commit()
    sqlHandle.close()
    print '---wheelspace_calibration over---'
    #-------------进入缓冲区---------------------------------------
    wheel_d2=3230-start_x  
    wheel_move_distance(robot,"front_distance",wheel_d2)
    sleep(22)
    #flagg,roomID=get_roomID(robot, item)
    
    flagw,roomID=read_wheelroomID(robot,'')    
    if flagw==-1 or flagw==3:   
        roomID='B1' 
    #-------------选择双目标定工位L0/R0-----------------------------
    if int(roomID[1])==2: #--- 到2排进行 双目标定
        Occupy_Num=0
        while 1:
            if Occupy_R0_Robot == "":
                wheel_move_angle(robot,"right_angle", 90)
                sleep(4)
                wheel_move_distance(robot,"front_distance",2410)
                sleep(17)
                wheel_move_angle(robot,"left_angle", 90)
                sleep(4)
                Occupy_R0_Robot=robot.robot_id
                print "Occupy_R0_Robot='%s'"%robot.robot_id
                break
            else:
                sleep(2)
                Occupy_Num+=1
                if Occupy_Num == 40 and Occupy_L0_Robot == "":
                    wheel_move_angle(robot,"left_angle", 90)
                    sleep(4)
                    wheel_move_distance(robot,"front_distance",2650)
                    sleep(17)
                    wheel_move_angle(robot,"right_angle", 90)
                    sleep(4)
                    Occupy_L0_Robot=robot.robot_id
                    print "Occupy_L0_Robot_except='%s'"%robot.robot_id
                    break
            if Occupy_Num > 300:
                print '等待工位超时'
                wing_move_angle(robot,"move",80)
                flag=3
                state['step_state'] = [2,2,2,2,2,3]
                update_robot_state(robot, item, flag, data,state)
                return 0
    else:   #--- 其他情况，全部到1排进行 双目标定
        Occupy_Num=0
        while 1:
            if Occupy_L0_Robot == "":
                wheel_move_angle(robot,"left_angle", 90)
                sleep(4)
                wheel_move_distance(robot,"front_distance",2650)
                sleep(17)
                wheel_move_angle(robot,"right_angle", 90)
                sleep(4)
                Occupy_L0_Robot=robot.robot_id
                print "Occupy_L0_Robot='%s'"%robot.robot_id
                break
            else:
                sleep(2)
                Occupy_Num+=1
                if Occupy_Num == 40 and Occupy_R0_Robot == "":
                    wheel_move_angle(robot,"right_angle", 90)
                    sleep(4)
                    wheel_move_distance(robot,"front_distance",2410)
                    sleep(17)
                    wheel_move_angle(robot,"left_angle", 90)
                    sleep(4)
                    Occupy_R0_Robot=robot.robot_id
                    print "Occupy_R0_Robot_except='%s'"%robot.robot_id
                    break
            if Occupy_Num > 300:
                print '等待工位超时'
                wing_move_angle(robot,"move",80)
                flag=3
                state['step_state'] = [2,2,2,2,2,3]
                update_robot_state(robot, item, flag, data,state)
                return 0
    if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
        del Occupy_infra_ultra_Road_Robot_List[0]
    flag = 2
    data[2] = roomID
    state['step_state'] = [2,2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
#*****************************************
# function:  excute_infra_ultra_calibration
# Date :
# Discription:   执行红外+超声 初始化(新版)
#*****************************************      
def excute_infra_ultra_calibration(robot, item, arg):
    global Occupy_infra_ultra_Road_Robot_List 
    flag = 1
    data = {}    
    state = {}
    state['step_name'] = [u"等待操作人员离开",u"初始化红外",u"初始化超声波",u"下一站"]
    udata=[]
    flagr,infra_ultrasonicinfo=read_configfile('init_infra_ultrasonic')
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
            del Occupy_infra_ultra_Road_Robot_List[0]
        return 0
    else:
        init_ultrasonic_Ld =  infra_ultrasonicinfo[0] 
        init_ultrasonic_Lin = infra_ultrasonicinfo[1]
    state['step_state'] = [1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------等待操作人员离开-----------
    print '\n','step1'
    wing_move_angle(robot,"move",30)
    sleep(3)
    flag = 1
    state['step_state'] = [2,1,0,0]
    update_robot_state(robot, item, flag, data, state)
    
    #2    
    #-----------初始化红外-----------
    print '\n','step2' 
    open_infrared_feedback(robot,0,'')
    sleep(1)
    infra_initflag,data[0]= open_infrared_feedback(robot,1,'')    
    flag = 1
    open_infrared_feedback(robot,0,'')              ####zc comment 关注下，设置初始化、数据反馈
    sleep(1)
    state['step_state'] = [2,1,1,0]  
    update_robot_state(robot, item, flag, data,state)
    #3
    #3-1-------初始化超声波-----------
    print '\n','step3-1'                
    sleep(2)
    ultra_initflag,ultrainitdata= execute_ultrasonic_init(robot)
    udata.append(ultrainitdata)
    data[1]=udata
    if ultra_initflag==-1 or ultra_initflag==3:
        flag=3        
        if infra_initflag==-1:            
            state['step_state'] = [2,3,3,0]            
        else:
            state['step_state'] = [2,2,3,0]
        wing_move_angle(robot,"move",80)
        update_robot_state(robot, item, flag, data,state)
        if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
            del Occupy_infra_ultra_Road_Robot_List[0]
        return 0
    flag = 1   
    #state['step_state'] = [2,1,1,0]
    state['step_state'] = [2,2,2,1] #--------------------------------------更改的
    update_robot_state(robot, item, flag, data,state)
    '''
    #3-2
    #-----------超声波 初始化 数据检验-----------
    print '\n','step3-2'
    sleep(1)
    ultraflag,ultradata= excute_Tultrasoniccalibration(robot,init_ultrasonic_Ld,init_ultrasonic_Lin)
    if ultraflag==-1:
        data[1]={}
    else:   
        print 'u0',ultradata[0],'u0type',type(ultradata[0])
        udata.append( ultradata[0])
        udata.append( ultradata[1])
        udata.append( ultradata[2])
        data[1]=udata        
    if ultraflag==-1 or ultraflag==3 :
        flag = 3
        if infra_initflag==-1:            
            state['step_state'] = [2,3,3,0]            
        else:
            state['step_state'] = [2,2,3,0]
        wing_move_angle(robot,"move",80)
        open_ultrasonic_feedback(robot,0,[0])
        sleep(2)
        update_robot_state(robot, item, flag, data,state)
        if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
            del Occupy_infra_ultra_Road_Robot_List[0]
        return 0
    if infra_initflag==-1:
        flag = 3
        state['step_state'] = [2,3,2,0]
        wing_move_angle(robot,"move",80)
        open_ultrasonic_feedback(robot,0,[0])
        sleep(2)
        update_robot_state(robot, item, flag, data,state)        
        if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
            del Occupy_infra_ultra_Road_Robot_List[0]
        return 0    
    open_ultrasonic_feedback(robot,0,[0])    
    flag = 1   
    state['step_state'] = [2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    '''
    #4
    #-----------下一站-----------#---------------------------------------------------------------------------------------------
    print '\n','step4'
    wing_move_angle(robot,"move",0)            
    sleep(2)
    flagw,roomID=read_wheelroomID(robot,'')    
    if flagw==-1:   
        roomID='B1'  #--- 可以直接 进行初始化（无需轮间距标定 选工位号）
        '''
        flag = 3
        state['step_state'] = [2,2,2,3]
        wing_move_angle(robot,"move",80)        
        update_robot_state(robot, item, flag, data,state)        
        return 0
        '''
    wheel_move_distance(robot,"front_distance",450)
    sleep(8)
    if int(roomID[1])==2: #--- 到2排进行 双目标定
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
        wheel_move_distance(robot,"front_distance",2410)
        sleep(17)
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
        
    else:   #--- 其他情况，全部到1排进行 双目标定
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
        wheel_move_distance(robot,"front_distance",2650)
        sleep(17)
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
        
    flag = 2    
    state['step_state'] = [2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    #+++退出抢占跑道队列+++++++++++
    if robot.robot_id in Occupy_infra_ultra_Road_Robot_List:
        del Occupy_infra_ultra_Road_Robot_List[0]
    print '---infra+ultrasonic init over---'    

    
#*****************************************
# function:  excute_binocular_calibration
# Date :
# Discription:   执行双目标定过程
#*****************************************  
def excute_camera_calibration(robot, item, arg):
    global Occupy_CL_Road_Robot_List
    global Occupy_CR_Road_Robot_List
    global Occupy_L0_Robot
    global Occupy_R0_Robot
    flag = 1
    data = {}
    state = {}
    camera_L={}
    camera_R={}
    state['step_name'] = [u"获取流程工位号",u"抢占跑道",u"拍照获取位置信息",u"运动到双目工位处",u"抓图",u"计算数据",u"抢占跑道",u"下一站"]    
    state['step_state'] = [1,0,0,0,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    sleep(0.5)
    #1
    #-----------获取流程工位号-----------
    print '\n','step1'
    #wing_move_angle(robot,"move",30)
    flagr,camerainfo=read_configfile('camera') #获取转台标定工位距离
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    else:
        camera_L[1] =  camerainfo[0] 
        camera_L[2] =  camerainfo[1]
        camera_L[3] =  camerainfo[2] 
        camera_L[4] =  camerainfo[3]
        camera_L[5] =  camerainfo[4] 
        camera_L[6] =  camerainfo[5]
        
        camera_R[1] =  camerainfo[6] 
        camera_R[2] =  camerainfo[7]
        camera_R[3] =  camerainfo[8] 
        camera_R[4] =  camerainfo[9]
        camera_R[5] =  camerainfo[10] 
        camera_R[6] =  camerainfo[11]        
    flagg,roomID=get_roomID(robot, item)
    if flagg==3 or flagg==(-1):
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    state['step_name'][0]=u"获取流程工位号：%s"%(roomID)
    state['step_state'] = [2,1,0,0,0,0,0,0]
    camera_take_pic(robot,'close')
    update_robot_state(robot, item, flag, data,state)


    
    #2
     #-----------抢占跑道-----------
    print '\n','step2'
    if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
        if not (robot.robot_id in Occupy_CL_Road_Robot_List):
            Occupy_CL_Road_Robot_List.append(robot.robot_id)#加入抢占左侧跑道队列
        #++++++滤波，等待，核实，决策+++++
        sleep(5)
        if robot.robot_id in Occupy_CL_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_CL_Road_Robot_List[0] == robot.robot_id:      
                    break #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [2,3,0,0,0,0,0,0]
                    update_robot_state(robot, item, flag, data,state)
                    return 0         
    elif roomID[0]=='R':
        if not (robot.robot_id in Occupy_CR_Road_Robot_List):
            Occupy_CR_Road_Robot_List.append(robot.robot_id)#加入抢占右侧跑道队列
        #++++++滤波，等待，核实，决策+++++
        sleep(5)
        if robot.robot_id in Occupy_CR_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_CR_Road_Robot_List[0] == robot.robot_id:
                    break   #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [2,3,0,0,0,0,0,0]
                    update_robot_state(robot, item, flag, data,state)
                    return 0
    flag=1
    state['step_state'] = [2,2,1,0,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #----------------释放双目工位R0/L0------------------
    if Occupy_R0_Robot == robot.robot_id:
        Occupy_R0_Robot=""
        print "'%s'release Occupy_R0_Robot"%robot.robot_id
    if Occupy_L0_Robot == robot.robot_id:
        Occupy_L0_Robot=""
        print "'%s'release Occupy_L0_Robot"%robot.robot_id
    
    #3
   #----------- 拍照获取位置信息 -----------
    print '\n','step3'
    if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
        cameraID='00453594'
        wheel_move_distance(robot,"front_distance",1470)
        sleep(14)
    elif roomID[0]=='R':
        cameraID='00327878'             #### zc comment 修改ID------------------------------------------------------------------ok
        wheel_move_distance(robot,"front_distance",1550)
        sleep(14)
    print 'cameraID:',cameraID
    flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok  
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,3,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0    
    flag = 1    
    state['step_state'] = [2,2,2,1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------运动到双目工位处（转台归位）-----------    
    print '\n','step4'
    if roomID[0]=='L':
        num=int(roomID[1])
        rotary_id='L'+str(num)
        camera_d=camera_L[num]        
    elif roomID[0]=='R':
        num=int(roomID[1])
        rotary_id='R'+str(num)
        camera_d=camera_R[num]

    start_x=info_start[0]
    start_y=info_start[1]
    start_angle=info_start[2]    
    
    if start_angle>0:
        angle_12 = 270-start_angle
        wheel_move_angle(robot,"right_angle",angle_12)
        sleep(6)
        wheel_d2=start_y
        if wheel_d2>10:
            wheel_move_distance(robot,"back_distance",wheel_d2)
        elif wheel_d2<-10:
            wheel_move_distance(robot,"front_distance",-wheel_d2)
        sleep(2)
        wheel_move_angle(robot,"right_angle",90)
            
    else:
        angle_13 = 270+start_angle
        wheel_move_angle(robot,"left_angle",angle_13)
        sleep(6)
        wheel_d2=start_y
        if wheel_d2>10:
            wheel_move_distance(robot,"front_distance",wheel_d2)
        elif wheel_d2<-10:
            wheel_move_distance(robot,"back_distance",-wheel_d2)
        sleep(2)
        wheel_move_angle(robot,"left_angle",90)
    sleep(3)
    if int(roomID[1])>=1 and int(roomID[1])<=3:                              #由于转台初始化需要sleep一下
        if int(roomID[1])==2 or (roomID[1])==3:
            flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok  
            if flagca==3:
                flag=3
                wing_move_angle(robot,"move",80)
                state['step_state'] = [2,2,2,3,0,0,0,0]
                update_robot_state(robot, item, flag, data,state)
                return 0
            start_angle=info_start[2]
            wheel_move_angle(robot,"right_angle",360-start_angle)
            sleep(10)
        wheel_d1=camera_d-start_x
        if wheel_d1>10:
            wheel_move_distance(robot,"front_distance",wheel_d1)
        elif wheel_d1<-10:
            wheel_move_distance(robot,"back_distance",-wheel_d1)
        move_time=wheel_d1/185+2
        sleep(move_time)
        print 'roomID\n'
        print roomID
        if roomID[0]=='L':
            wheel_move_angle(robot,"right_angle", 90)
            sleep(4)
            wheel_d2=1200+start_y
            wheel_move_distance(robot,"front_distance",wheel_d2)
        else:
            wheel_move_angle(robot,"left_angle", 90)
            sleep(4)
            wheel_d2=1200-start_y
            wheel_move_distance(robot,"front_distance",wheel_d2)
        sleep(14)
    if int(roomID[1])>=4 and int(roomID[1])<=6:
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok  
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,3,0,0,0,0]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_angle=info_start[2]
        print "self turn:",start_angle
        wheel_move_angle(robot,"right_angle",360-start_angle)
        sleep(10)
        if   roomID[0]=='L':  #--- 写入左右侧 的相机ID号
            cameraID='00323320'             #----------------------------------------------------ok
        elif roomID[0]=='R':
            cameraID='00402546'              #### zc comment 修改ID-------------------------------------------ok
        wheel_d3=4650-start_x
        wheel_move_distance(robot,"front_distance",wheel_d3)
        move_time=wheel_d3/185+2
        sleep(move_time)
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')    #---------------------------------------ok
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,3,0,0,0,0]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_x=info_start[0]
        start_y=info_start[1]
        start_angle=info_start[2]   
        
        if start_angle>0:
            angle_12 = 360-start_angle
            wheel_move_angle(robot,"right_angle",angle_12)
        else:
            angle_13 = 360+start_angle
            wheel_move_angle(robot,"left_angle",angle_13)        
        sleep(10)
        wheel_d1=camera_d-start_x
        if wheel_d1>10:
            wheel_move_distance(robot,"front_distance",wheel_d1)
        elif wheel_d1<-10:
            wheel_move_distance(robot,"back_distance",-wheel_d1)
        move_time=wheel_d1/185+2
        sleep(move_time)
        if roomID[0]=='L':
            wheel_move_angle(robot,"right_angle", 90)
            sleep(4)
            wheel_d2=1200+start_y
            wheel_move_distance(robot,"front_distance",wheel_d2)
        else:
            wheel_move_angle(robot,"left_angle", 90)
            sleep(4)
            wheel_d2=1200-start_y
            wheel_move_distance(robot,"front_distance",wheel_d2)
        sleep(14) 
    state['step_state'] = [2,2,2,2,1,0,0,0]
    update_robot_state(robot, item, flag, data, state)
    #+++退出抢占跑道队列+++++++++++
    if roomID[0]=='L':
        if robot.robot_id in Occupy_CL_Road_Robot_List:
            del Occupy_CL_Road_Robot_List[0]
    elif roomID[0]=='R':
        if robot.robot_id in Occupy_CR_Road_Robot_List:
            del Occupy_CR_Road_Robot_List[0]



    #5
    #-----------抓图-----------
    print '\n','step5'

    #-----------调整小胖位置-----------

    posiflag,data=get_rotate_platform_position(robot)
    print "posiflag=%d"%posiflag
    if posiflag==-1:
        flag = 3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,2,3,0,0,0]         
        update_robot_state(robot, item, flag, data,state)
        return 0
    if data[0]==1:
        angle=data[1]
        rotate_platform_angle=-data[2]
        print "rotate_platform_angle=%d"%rotate_platform_angle
        if angle>1:
            wheel_move_angle(robot,"right_angle",angle)
            sleep(3)
        elif angle<-1:
            wheel_move_angle(robot,"left_angle",-angle)
            sleep(3)
    else:
        logger.error('rotate platform position picture error')
        flag = 3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,2,3,0,0,0]         
        update_robot_state(robot, item, flag, data,state)
        camera_take_pic(robot,'close')
        return 0
    checflag,data=get_check_location_picture(robot)
    if checflag==-1:
        flag = 3
        wing_move_angle(robot,"move",80)
        camera_take_pic(robot,'close')
        state['step_state'] = [2,2,2,2,3,0,0,0]         
        update_robot_state(robot, item, flag, data,state)
        return 0
    if data[0]==1:
        flag=1
    else:
        logger.error('check_location_picture info error')
        flag = 3
        wing_move_angle(robot,"move",80)
        camera_take_pic(robot,'close')
        state['step_state'] = [2,2,2,2,3,0,0,0]         
        update_robot_state(robot, item, flag, data,state)
        return 0



    rotary_flag= rotary_controller(rotary_id,0,rotate_platform_angle) 
    if rotary_flag==3:
        flag = 3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,2,3,0,0,0]        
        update_robot_state(robot, item, flag, data,state)
        return 0    
    sleep(4)
    


    rotary_controller(rotary_id,32.5,32.5+rotate_platform_angle)
    sleep(4)
    cameraflag=camera_calibration_process(robot,rotary_id,rotate_platform_angle)#-----------------------------------------------------------------------------------------------------
    if cameraflag==-1 :
        flag = 3
        wing_move_angle(robot,"move",80)
        rotary_controller(rotary_id,0,0)
        camera_take_pic(robot,'close')
        sleep(1)
        state['step_state'] = [2,2,2,2,3,0,0,0]        
        update_robot_state(robot, item, flag, data,state)
        return 0
    
    state['step_state'] = [2,2,2,2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)

    wheel_move_angle(robot,"left_angle", 180)
    sleep(9)


    #6
    #-----------计算数据-----------
    print '\n','step6'
    rotary_controller(rotary_id,0,0)
    
    camdealflag,data=camera_deal_data(robot)
    camera_take_pic(robot,'close')
    if camdealflag==-1:
        flag = 3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,2,2,2,3,0,0]        
        update_robot_state(robot, item, flag, data,state)
        return 0
    state['step_state'] = [2,2,2,2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)

    
    #7
    #-----------抢占跑道-----------
    print '\n','step7'
    if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
        if not (robot.robot_id in Occupy_CL_Road_Robot_List):
            Occupy_CL_Road_Robot_List.append(robot.robot_id)#加入抢占左侧跑道队列
        #++++++滤波，等待，核实，决策+++++
        sleep(5)
        if robot.robot_id in Occupy_CL_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_CL_Road_Robot_List[0] == robot.robot_id:     
                    break #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [2,2,2,2,2,2,3,0]
                    update_robot_state(robot, item, flag, data,state)
                    return 0         
    elif roomID[0]=='R':
        if not (robot.robot_id in Occupy_CR_Road_Robot_List):
            Occupy_CR_Road_Robot_List.append(robot.robot_id)#加入抢占右侧跑道队列
        #++++++滤波，等待，核实，决策+++++
        sleep(5)
        if robot.robot_id in Occupy_CR_Road_Robot_List:
            occ=0
            while 1: #循环等待抢占结果
                if Occupy_CR_Road_Robot_List[0] == robot.robot_id:
                    break   #直到抢占列表轮转到当前小胖跳槽循环
                sleep(2)
                occ += 1
                if occ>300:
                    print '等待抢占超时'
                    wing_move_angle(robot,"move",80)
                    flag=3
                    state['step_state'] = [2,2,2,2,2,2,3,0]
                    update_robot_state(robot, item, flag, data,state)
                    return 0
    flag=1
    state['step_state'] = [2,2,2,2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    #8
    #-----------下一站-----------
    print '\n','step8'
    wing_move_angle(robot,"move",0)
    
    wheel_move_distance(robot,"front_distance",1200)
    sleep(9)
    if roomID[0]=='R':
        wheel_move_angle(robot,"left_angle", 90)
    else:
        wheel_move_angle(robot,"right_angle", 90)
    sleep(4)
    #-------------让出工位---------------------------------------
    sqlHandle = sqlite3.connect(DATABASE_PATH)
    sqlInterface = sqlHandle.cursor()
    #sql = 'DELETE FROM robot_room WHERE robot_id = "%s" ' % (robot_id)
    sql = 'update robot_room set roomID = "%s" where robot_id = "%s"' % ('Y'+roomID[1], robot.robot_id)
    sqlHandle.execute(sql)
    sqlHandle.commit()
    sqlHandle.close()
    print '---wheelspace_calibration over---'
    #------------------------------------------------------------
    if int(roomID[1])==1:
        #----------- 拍照获取位置信息 -----------
        if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
            cameraID='00453594'
        elif roomID[0]=='R':
            cameraID='00327878'             #### zc comment 修改ID------------------------------------------------------------------ok
        print 'cameraID:',cameraID
        #flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,2,2,2,2,2]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_x=info_start[0]
        start_y=info_start[1]
        start_angle=info_start[2]
        if start_angle>0:
            angle_12 = 360-start_angle
            wheel_move_angle(robot,"right_angle",angle_12)
        else:
            angle_13 = 360+start_angle
            wheel_move_angle(robot,"left_angle",angle_13)        
        sleep(10)
        wheel_d1=4650-camera_d-start_x
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
        if roomID[0]=='L':  
            cameraID='00323320'
        elif roomID[0]=='R':
            cameraID='00402546'            
        print 'cameraID:',cameraID
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,2,2,2,2,2]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_x=info_start[0]
        start_y=info_start[1]
        start_angle=info_start[2]
        if start_angle>0:
            angle_12 = 360-start_angle
            wheel_move_angle(robot,"right_angle",angle_12)
        else:
            angle_13 = 360+start_angle
            wheel_move_angle(robot,"left_angle",angle_13)        
        sleep(10)
        wheel_d1=4900-start_x
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
    elif int(roomID[1])==2 or int(roomID[1])==3:
        wheel_d1=4650-camera_d
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
        #----------- 拍照获取位置信息 -----------
        if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
            cameraID='00323320'
        elif roomID[0]=='R':
            cameraID='00402546'             #### zc comment 修改ID------------------------------------------------------------------ok
        print 'cameraID:',cameraID
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok  
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,2,2,2,2,2]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_x=info_start[0]
        #start_y=info_start[1]
        start_angle=info_start[2]
        if start_angle>0:
            angle_12 = 360-start_angle
            wheel_move_angle(robot,"right_angle",angle_12)
        else:
            angle_13 = 360+start_angle
            wheel_move_angle(robot,"left_angle",angle_13)        
        sleep(10)
        wheel_d1=4900-start_x
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
    if int(roomID[1])==4:
        #----------- 拍照获取位置信息 -----------
        if roomID[0]=='L':  #--- 写入左右侧 的相机ID号---------------------------------------------------------------------------------ok
            cameraID='00323320'
        elif roomID[0]=='R':
            cameraID='00402546'             #### zc comment 修改ID------------------------------------------------------------------ok
        print 'cameraID:',cameraID
        flagca,info_start=get_camera_info(cameraID,'pos_angle','192.168.5.113')  #------------------------------------------------------------ok  
        if flagca==3:
            flag=3
            wing_move_angle(robot,"move",80)
            state['step_state'] = [2,2,2,2,2,2,2,2]
            update_robot_state(robot, item, flag, data,state)
            return 0
        start_x=info_start[0]
        #start_y=info_start[1]
        start_angle=info_start[2]
        if start_angle>0:
            angle_12 = 360-start_angle
            wheel_move_angle(robot,"right_angle",angle_12)
        else:
            angle_13 = 360+start_angle
            wheel_move_angle(robot,"left_angle",angle_13)        
        sleep(10)
        wheel_d1=4900-start_x
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
    if int(roomID[1])==5 or int(roomID[1])==6:
        wheel_d1=4900-camera_d
        wheel_move_distance(robot,"front_distance",wheel_d1)
        move_time=wheel_d1/185+3
        sleep(move_time)
    #+++退出抢占跑道队列+++++++++++
    if roomID[0]=='L':
        if robot.robot_id in Occupy_CL_Road_Robot_List:
            del Occupy_CL_Road_Robot_List[0]
    elif roomID[0]=='R':
        if robot.robot_id in Occupy_CR_Road_Robot_List:
            del Occupy_CR_Road_Robot_List[0]
            
    if roomID[0]=='L':
        wheel_move_angle(robot,"right_angle", 90)
        sleep(4)
        wheel_move_distance(robot,"front_distance",3400-800)
        sleep(20)
        #wheel_move_angle(robot,"left_angle", 90)
        #sleep(4)
    else:
        wheel_move_angle(robot,"left_angle", 90)
        sleep(4)
        wheel_move_distance(robot,"front_distance",1600-800)
        sleep(11)
        #wheel_move_angle(robot,"right_angle", 90)
        #sleep(4)
    '''
    wheel_move_distance(robot,"front_distance",1840)
    sleep(12)
    wheel_move_angle(robot,"left_angle", 90)
    sleep(4)
    wheel_move_distance(robot,"back_distance",1150)
    sleep(9)
    '''
    flag = 2    
    state['step_state'] = [2,2,2,2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state) 
    print '---camera_calibration over---'
#*****************************************
# function:  excute_move_check_calibration
# Date :
# Discription:   执行行走航位检测过程
#*****************************************  
def excute_move_check_calibration(robot, item,arg):
    flag = 1
    data={}
    state = {}
    state['step_name'] = [u"获取相机数据",u"行走5米",u"获取相机数据",\
                          u"校验数据",u"下一站"]
    '''
    flagr,odometerinfo=read_configfile('odometer')
    if flagr==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    else:
        odometer_d1 =  odometerinfo[0] 
        odometer_wheelbase =  odometerinfo[1]
    '''
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    wing_move_angle(robot,"move",0)
    sleep(2)
    open_navigation_switch(robot,"stop",'')
    set_navigation(robot, 0, 0, 0)
    sleep(2)    
    flagca,y_start=get_camera_info('00361432','pos','192.168.6.114')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1    
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #2
    #-----------行走5米-----------
    print '\n','step2'    
    wheel_move_distance(robot,"front_distance",5000)            
    sleep(30)
    flag = 1    
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    sleep(2)
    flagca,y_end=get_camera_info('00384058','pos','192.168.6.114')    
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [2,2,3,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1    
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------计算下载数据-----------
    print '\n','step4'
    odoflag,odometer_y =open_navigation_switch(robot,"start",'')
    if odoflag==-1:
        flag=3
        wing_move_angle(robot,"move",80)
        open_navigation_switch(robot,"stop",'')
        sleep(2)
        state['step_state'] = [2,2,2,3,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    open_navigation_switch(robot,"stop",'')
    delta = float(y_end-y_start)    
    ododelta=odometer_y-delta    
    data[1]= delta  ;#1--- 行走 偏差
    data[2]= odometer_y ;#2--- 航位 值
    data[3]= ododelta  ;#3--- 航位 偏差
    print '1delta=',delta
    print '2odometer_y =',odometer_y
    print '3ododelta=',ododelta
    
    #--- 行走 偏差值 大于 300 就失败（代表 行走控制 有问题！）    
    if abs(delta) >100:                                        #300--------3000改回来---------------------------------------------------------------------------------
        flag=3
        wing_move_angle(robot,"move",80)
        open_navigation_switch(robot,"stop",'')
        sleep(2)              
        state['step_state'] = [2,2,2,3,0]
        update_robot_state(robot, item, flag, data,state)
        return 0    
    sleep(2)    
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'    
    wing_move_angle(robot,"move",0)  
    sleep(2)
    flag = 2
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---odometer_calibration over---'
#*****************************************
# function:  excute_wheelspace_check_calibration
# Date :
# Discription:   执行 轮间距检测 过程
#*****************************************  
def excute_wheelspace_check_calibration(robot, item, arg):    
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state = {}
    state['step_name'] = [u"获取相机数据",u"转动5圈",u"获取相机数据",\
                          u"校验数据",u"下一站"]
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    sleep(3)
    flagca,theta_start=get_camera_info('00384058','angle','192.168.6.114')
    print 'camera con'   
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(3)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #2
    #-----------转动5圈-----------
    print '\n','step2'
    n=5
    wheel_move_angle(robot,"right_angle",n*360)           
    sleep(40)
    print '++++++yyyyy++++++++'
    flag = 1
    data = [1,1,1,1,0,0,0,0] 
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    flagca,theta_end=get_camera_info('00384058','angle','192.168.6.114')
    if flagca==3:
        flag=3
        wing_move_angle(robot,"move",80)
        state['step_state'] = [3,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(3)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------校验数据-----------
    print '\n','step4'
    R_angle= float(theta_end+n*360-theta_start)
    V_angle = n*360
    k = V_angle/R_angle
    if abs(k-1)>0.005:
        flag = 3
        state['step_state'] = [2,2,2,3,0]
        update_robot_state(robot, item, flag, data,state)
        return 0
    sleep(2)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'    
    wing_move_angle(robot,"move",30)                       
    sleep(3)
    wheel_move_distance(robot,"front_distance",1000)            
    sleep(6)
    flag = 2
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---wheelspace_calibration over---'
     
#*****************************************
# function:  excute_camera_first_calibration
# Date :
# Discription:   执行新双目标定过程
# 2017年1月13日 liyao
#*****************************************  
def excute_camera_first_calibration(robot, item, arg):
    flag = 3
    data = {}    
    state = {}
    state['step_name'] = [u"打开摄像头",u"标定图1",u"标定图2",u"标定图3",u"标定图4",u"标定图5",u"标定图6",u"标定图7",u"下一站"]    
    state['step_state'] = [1,0,0,0,0,0,0,0,0]
    slipway_offset = 0.0
    pic_n = 1
    fail_cnt = 0;
    #step1 打开摄像头
    camera_take_pic(robot,'open_camera');
    #robot.connectTCP.clean() 
    if get_json_state(robot, 'data', 'camera', 'state') == 0:
        state['step_state'] = [3,0,0,0,0,0,0,0,0]
        update_robot_state(robot, item, flag, data,state)
        print '打开摄像头失败\n'
        return 0; 
    state['step_state'][0] = 2
    sleep(2)
    #step2 拍摄图片
    while 1:
        set_picn_location(robot, pic_n)#发送图片序号并请求获取滑台位置
        
        ret = get_slipway_location(robot) #获取滑台偏移量
        if ret == 'fail' : 
            state['step_state'][pic_n] = 3
            update_robot_state(robot, item, 3, data,state)
            print '第%d张图获取滑台偏移位置失败\n'%pic_n
            return 0
        slipway_offset = float(ret)
        if slipway_offset == 0 :
            print '开始保存图片\n'
            fail_cnt = 0
            camera_take_pic(robot,'photograph');#拍摄并保存图片
            #sleep(4)
            if get_json_state(robot, 'data', 'camera', 'state') == 1:
                state['step_state'][pic_n] = 2
                update_robot_state(robot, item, 2, data,state)
                print '保存成功进行下一步\n'
            else:
                state['step_state'][pic_n] = 3
                update_robot_state(robot, item, 3, data,state)
                print '图片保存失败\n'
                return 0    
            print '第%d张照片标定完毕\n'%pic_n
            if pic_n == 7 :#拍照结束
                break;
            else:
                pic_n += 1
                continue
        else:
            if fail_cnt == 3 :#调整失败次数满足
                state['step_state'][pic_n] = 3
                update_robot_state(robot, item, flag, data,state)
                print '转台调整3次未到位 标定失败\n'
                return 0
            rotary_flag= slipstage_controller(slipway_offset,100) #控制滑台运动到指定位置 
            if rotary_flag==3:
                flag = 3
                wing_move_angle(robot,"move",80)
                state['step_state'][pic_n] = 3
                update_robot_state(robot, item, 3, data,state)
                print '滑台调整失败\n'
                return 0
            sleep(3)
            fail_cnt += 1
            continue 
    state['step_state'][pic_n+1] = 2 
    update_robot_state(robot, item, 2, data,state)    
    print '拍照标定结束\n'
    return 1       
    
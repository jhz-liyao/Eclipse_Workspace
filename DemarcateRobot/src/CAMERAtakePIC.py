# -*- coding: utf-8 -*-
from protocol import *
from formula  import *
import sqlite3
from sys_env import *
from time import *
from state import *
#*****************************************
# function:  process
# Date :
# Discription:   执行各个标定过程
#*****************************************  
def excute_process(robot, item):
    print item
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
    #STEP6
    #+++++++++++++++infrared +++++++++++++++++++++++++++++++++++++++++
    if item == 'infrared':
        excute_process_calibration(excute_infrared_calibration,robot, item,'')
    #STEP7
    #+++++++++++++++ultrasonic +++++++++++++++++++++++++++++++++++++++++
    if item == 'ultrasonic':
        excute_process_calibration(excute_ultrasonic_calibration,robot, item,'')         
            
def excute_process_calibration(_fun,robot, item, arg):
    st = ''
    st = get_robot_state(robot, item)
    if st['flag']==3:
        data = set_process_state(0,[],{})
        reset_process(robot.robot_id,item,data)
    st = get_robot_state(robot, item)
    if st['flag']==0:        
        process_state = get_process_state(item)
        print process_state
        if not 'robot_id' in process_state:
            print 'lll0000'
            state = {'robot_id':robot.robot_id}
            update_process_state(robot,item,state)
            _fun(robot, item,'')
            state = {}
            update_process_state(robot,item,state)
        elif process_state['robot_id'] == robot.robot_id:
            print 'lll222'
            state = {'robot_id':robot.robot_id}
            update_process_state(robot,item,state)
            _fun(robot, item, arg)
            state = {}
            update_process_state(robot,item,state)
            
           

#*****************************************
# function:  excute_move_calibration
# Date :
# Discription:   执行行走控制标定过程
#*****************************************  
def excute_move_calibration(robot,item,arg):
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state = {}
    state['step_name'] = [u"获取相机数据",u"行走5米",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    sleep(3)
    y_start=get_camera_info('00263780','pos','192.168.1.110')
    sleep(2)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)    
    #2
    #-----------行走5米-----------
    print '\n','step2'
    wheel_move_distance(robot,"front_distance",5000)            
    sleep(28)
    flag = 1
    data = [1,1,1,1,0,0,0,0] 
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    y_end=get_camera_info('00399800','pos','192.168.1.110')              
    sleep(2)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------计算下载数据-----------
    print '\n','step4'
    delta = float(y_end-y_start) 
    [k,th,R] = calc_motor_control_compensation(delta,5000,447)
    print k
    if delta > 0:
        data = [k,1,1,1,1,0,0,0,0,0]
    else:
        data = [1,1,k,1,1,0,0,0,0,0]
    set_motorcomp(robot, 1, data)
    flag = 1
    sleep(2)
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'
    wheel_move_angle(robot,"left_angle",90)                     
    sleep(6)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-2
    #-----------下一站-----------
    wheel_move_distance(robot,"front_distance",1700)            
    sleep(12)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-3
    #-----------下一站-----------
    wheel_move_angle(robot,"left_angle",90)            
    sleep(6)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-4
    #-----------下一站-----------
    wheel_move_distance(robot,"back_distance",500)            
    sleep(8)
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
    data = [1,1,1,1,0,0,0,0]
    state = {}
    state['step_name'] = [u"获取相机数据",u"行走5米",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    set_navigation(robot, 0, 0, 0)
    sleep(2) 
    y_start=get_camera_info('00366817','pos','192.168.1.111')  
    sleep(2)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #2
    #-----------行走5米-----------
    print '\n','step2'
    wheel_move_distance(robot,"front_distance",5730)            
    sleep(35)
    flag = 1
    data = [1,1,1,1,0,0,0,0] 
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    sleep(2)
    y_end=get_camera_info('00408370','pos','192.168.1.111')
    sleep(2)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------计算下载数据-----------
    print '\n','step4'
    odometer_y =open_navigation_switch(robot,"start",'')
    print 'odometer_y =',odometer_y
    delta = float(y_end-y_start)    
    delta1=odometer_y-delta    
    [k,th,R] = calc_DeadReckoning_compensation(delta1,5730,447)
    print k
    if delta > 0:
        data = [k,1,1,1,1,0,0,0,0,0]
    else:
        data = [1,k,1,1,1,0,0,0,0,0]
    set_motorcomp(robot, 3, data)
    sleep(2)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'    
    wing_move_angle(robot,"move",30)                           
    sleep(3)
    wing_move_angle(robot,"move",0)                           
    sleep(3)
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
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state = {}
    state['step_name'] = [u"获取相机数据",u"转动10圈",u"获取相机数据",\
                          u"计算下载数据",u"下一站"]
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------获取相机数据-----------
    print '\n','step1'
    sleep(3)
    theta_start=get_camera_info('200408370','angle','192.168.1.111')
    print 'camera con'
    sleep(3)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #2
    #-----------转动10圈-----------
    print '\n','step2'
    n=10
    wheel_move_angle(robot,"right_angle",n*360)           
    sleep(80)
    print '++++++yyyyy++++++++'
    flag = 1
    data = [1,1,1,1,0,0,0,0] 
    state['step_state'] = [2,2,1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------获取相机数据-----------
    print '\n','step3'
    theta_end=get_camera_info('200408370','angle','192.168.1.111')
    sleep(3)
    flag = 1
    data = [1,1,1,1,0,0,0,0]
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------计算下载数据-----------
    print '\n','step4'
    R_angle = float(theta_end+n*360-theta_start)
    V_angle = n*360
    k = V_angle/R_angle
    data = [447*k,0,0,0,0,0,0,0,0,0]
    set_motorcomp(robot, 4, data)
    sleep(2)
    flag = 1
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #5-1
    #-----------下一站-----------
    print '\n','step5'    
    wing_move_angle(robot,"move",30)                       
    sleep(3)
    flag = 2
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---wheelspace_calibration over---'

#*****************************************
# function:  excute_infra_ultra_calibration(robot, item, '')
# Date :
# Discription:   执行超声、红外初始化
#*****************************************      
def excute_infra_ultra_calibration(robot, item, arg):
    flag = 1
    data = {}
    state = {}
    state['step_name'] = [u"等待操作人员离开",u"初始化超声波",u"初始化红外",u"超声波远距离标定",u"下一站"]
    state['step_state'] = [1,0,0,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------等待操作人员离开-----------
    print '\n','step1'
    sleep(5)
    flag = 1
    state['step_state'] = [2,1,0,0,0]
    update_robot_state(robot, item, flag, data, state)
    #2-------初始化超声波-----------
    print '\n','step2'
    wing_move_angle(robot,"move",30)            
    sleep(3)
    data[0]= execute_ultrasonic_init(robot)
    flag = 1   
    state['step_state'] = [2,2,1,0,0]    
    update_robot_state(robot, item, flag, data,state)    
    #3    
    #-----------初始化红外-----------
    print '\n','step3'                
    sleep(3)
    open_infrared_feedback(robot,0,'')
    sleep(1)
    data[1]= open_infrared_feedback(robot,1,'')
    flag = 1    
    state['step_state'] = [2,2,2,1,0]
    update_robot_state(robot, item, flag, data,state)    
    #4
    #-----------超声波远距离 标定-----------
    print '\n','step4'                
    sleep(3)
    tempdata1= open_ultrasonic_feedback(robot,8191,[13])    
    sleep(5)
    open_ultrasonic_feedback(robot,0,[0])
    sleep(2)
    wheel_move_angle(robot,"left_angle",180)
    sleep(9)
    tempdata2= open_ultrasonic_feedback(robot,8191,[13])    
    sleep(5)
    open_ultrasonic_feedback(robot,0,[0])
    sleep(2)
    flag2,Trcv= judge_ultrasonic_data(str(tempdata1), str(tempdata2),1500, '')    
    data[2]=Trcv
    print 'Trcv=',data[2]
    state['step_state'] = [2,2,2,2,1]
    update_robot_state(robot, item, flag, data,state)    
    #5
    #-----------下一站-----------
    print '\n','step5'
    wing_move_angle(robot,"move",0)            
    sleep(3)
    flag = 2    
    state['step_state'] = [2,2,2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---infraultra_init over---'
    
#*****************************************
# function:  excute_ultrasonic_calibration
# Date :
# Discription:   执行超声标定过程
#*****************************************  
def excute_ultrasonic_calibration(robot, item, arg):
    flag = 1
    data = []
    state = {}
    state['step_name'] = [u"操作人员离开",u"短距离校验",u"下一站"]
    state['step_state'] = [1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------等待操作人员离开-----------
    print '\n','step1'
    sleep(6)
    flag = 1
    data = []
    state['step_state'] = [2,1,0]
    update_robot_state(robot, item, flag, data, state)
    #2    
    #-----------短距离校验-----------
    print '\n','step2'
    data= excute_ultrasoniccalibration(robot,'')          
    sleep(10)
    flag = 1   
    state['step_state'] = [2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------下一站-----------
    print '\n','step3'
    wheel_move_angle(robot,"left_angle",90)            
    sleep(4)
    flag = 2    
    state['step_state'] = [2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---ultrasonic_calibration over---'
    
#*****************************************
# function:  excute_infrared_calibration
# Date :
# Discription:   执行红外标定过程
#*****************************************  
def excute_infrared_calibration(robot, item, arg):
    flag = 1
    data = {}
    state = {}
    state['step_name'] = [u"操作人员离开",u"障碍物校验",u"下一站"]
    state['step_state'] = [1,0,0]
    update_robot_state(robot, item, flag, data,state)
    #1
    #-----------等待操作人员离开-----------
    print '\n','step1'
    sleep(6)
    flag = 1    
    state['step_state'] = [2,1,0]
    update_robot_state(robot, item, flag, data, state)
    #2
    #-----------障碍物校验-----------
    print '\n','step2'
    infradata= get_infrared_statusfeed(robot,1,'')
    print 'infradata= ',infradata
    sleep(1)
    get_infrared_statusfeed(robot,0,'') 
    flag = 1
    data = infradata
    state['step_state'] = [2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #3
    #-----------下一站-----------
    print '\n','step3'
    wheel_move_distance(robot,"back_distance",100)            
    sleep(5)
    flag = 2    
    state['step_state'] = [2,2,2]
    update_robot_state(robot, item, flag, data,state)
    print '---infrared_calibration over---'
    
#*****************************************
# function:  excute_binocular_calibration
# Date :
# Discription:   执行双目标定过程
#*****************************************  
def excute_camera_calibration(robot, item, arg):
    flag = 1
    data = {}
    state = {}
    state['step_name'] = [u"等待操作人员离开",u"抓图",u"计算数据",u"下一站"]
    state['step_state'] = [1,0,0,0]
    update_robot_state(robot, item, flag, data,state)    
    #1
    #-----------等待操作人员离开（转台归位）-----------
    #转台归位
    print '\n','step1'    
    rotary_controller('001',100,35)
    wing_move_angle(robot,"move",30)
    sleep(22) 
    state['step_state'] = [2,1,0,0]
    update_robot_state(robot, item, flag, data, state)
    #2
    #-----------抓图-----------
    print '\n','step2'
    camera_calibration_process(robot)    
    state['step_state'] = [2,2,1,0]
    update_robot_state(robot, item, flag, data,state)    
    #3
    #-----------计算数据-----------
    print '\n','step3'
    data=camera_deal_data(robot) 
    state['step_state'] = [2,2,2,1]
    update_robot_state(robot, item, flag, data,state)
    #4
    #-----------下一站-----------
    print '\n','step4'
    wing_move_angle(robot,"move",0)            
    sleep(3)
    flag = 2    
    state['step_state'] = [2,2,2,2]
    update_robot_state(robot, item, flag, data,state)    
    print '---camera_calibration over---'
    
#--------------------主函数-----------------------------

if __name__ == '__main__':
    #raw_input('ready start>')
    i=0
    while i<1:
        i=1
        N=raw_input(unicode('请输入运行的程序编号:','utf-8').encode('gbk'))        
        if N=='1':
            print 'start'            
            robot=Robots(u'123',u'192.168.1.12',9010)
            print '11'
            get_robot_connection_state(robot)
            print '22'           
                        
            data = [1,1,1,1,1,0,0,0,0,0]
            set_motorcomp(robot, 1, data)
            #switch_obstacle_status(robot,0,'')
            sleep(8)
            wheel_move_distance(robot,"front_distance",5000) 
            #sleep(3)
            raw_input( 'excute process>')
            
        elif N=='2':

            #-----------行走控制标定-----------
            #rcv=get_camera_info('00263780','angle','192.168.1.110')
            for j in range(1):
                #wheel_move_angle(robot,"right_angle",0)
                #sleep(3) 
                #fl,rcv=get_camera_info('00263780','pos','192.168.1.110')
                #fl,rcv=get_camera_info('00399800','pos','192.168.1.110')
                #fl,rcv=get_camera_info('00366817','pos','192.168.1.111')
                #fl,rcv=get_camera_info('00408370','pos','192.168.1.111')
                
                #fl,rcv=get_camera_info('00323320','pos','192.168.1.112')
                #fl,rcv=get_camera_info('00453594','pos','192.168.1.112')
                fl,rcv=get_camera_info('00289713','pos','192.168.1.112')
                
                print rcv

            #-----------行走控制标定相机标定-----------
            #wheel_camera_calibration('100263780','100399800')
            #----------行走航位标定相机标定----------------
            #wheel_camera_calibration('100263780','100399800')
                
            #----------行走航位标定----------------
            #rcv=get_camera_info('00366817','pos','192.168.1.111')
            #rcv=get_camera_info('00408370','pos','192.168.1.111')
        else:
            print u'输入编号错误！'
    




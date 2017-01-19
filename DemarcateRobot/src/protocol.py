# -*- coding: utf-8 -*-
#==============================================================================
# Group:   JHZ-Robot
# Project: Motor Calibration
# File :   protocol.py
# Date :   2016-01-07
# Discription :
#          server2robot protocol.
#==============================================================================

from sys_env import *
import json
from fetch_camera_data import *
from mylog import*
import time
from app_config import *
from time import *

#---------------------global param-----------------------------------------------
cmd_connect_header = '{"module_id":10000006,"module_name":"video","action_name":\
"com.efrobot.VIDEO","data_extra_name":"data","isIgnoreMaskState":true,\
"data":{}}\r\n'
cmd_move_header = '"module_id":11000006,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_setmotorcomp_header = '"module_id":11000007,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_setnavigation_header = '"module_id":11000008,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_navigation_header = '"module_id":11000009,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'

cmd_camera_header = '"module_id":11000010,"module_name":"camera","action_name":\
"com.efrobot.robot.CAMERA","data_extra_name":"camera"'
cmd_ultrasonic_init_header = '"module_id":11000013,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_ultrasonic_data_header = '"module_id":11000014,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_infrared_data_header = '"module_id":11000015,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_obstacle_status_header = '"module_id":11000017,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_movepoint_header = '"module_id":11000023,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'
cmd_infra_statusfeedback_header = '"module_id":11000029,"module_name":"control","action_name":\
"com.efrobot.robot.CONTROL","data_extra_name":"robotControl"'

#*****************************************
# function:   get_robot_connection_state
# Date :
# Discription:
#*****************************************
def get_robot_connection_state(robot):
    robot.connectTCP.send(cmd_connect_header)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv1:'+rcv
    if rcv !='':
        rcv_json = json.loads(rcv)
        print rcv_json['response_code']
        return rcv_json['response_code']
    return 1

#*****************************************
# function:   wheel_move_distance
# Date :
# Discription:
#*****************************************
def wheel_move_distance(robot,direction,distance):
    cmd_content = '"data":{"wheel":{"direction":"'+direction+'","distance":'+str(distance)+'}}'
    cmd = "{" + cmd_move_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv2:' + rcv

#*****************************************
# function:   wheel_move_angle
# Date :
# Discription:
#*****************************************
def wheel_move_angle(robot,direction,angle):
    cmd_content = '"data":{"wheel":{"direction":"'+direction+'","angle":'+str(angle)+'}}'
    cmd = "{" + cmd_move_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv2:' + rcv

#*****************************************
# function:   wheel_move
# Date :
# Discription:
#*****************************************
def wheel_move(robot,direction,speed):
    cmd_content = '"data":{"wheel":{"direction":"'+direction+'","speed":'+str(speed)+'}}'
    cmd = "{" + cmd_move_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv2:' + rcv
    
#*****************************************
# function:   wing_move_angle
# Date :
# Discription:
#*****************************************
def wing_move_angle(robot,direction,angle):   
    cmd_content = '"data":{"wing":{"direction":"'+direction+'","angle":'+str(angle)+'}}'
    cmd = "{" + cmd_move_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv2:' , rcv

#*****************************************
# function:   set_motorcomp
# Date :
# Discription:
#*****************************************
def set_motorcomp(robot, stp, data):
    cmd_content = '"data":{"parameter_type":{"type":'+str(stp)+',"par_array":'+str(data)+'}}'
    cmd = "{" + cmd_setmotorcomp_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv1:' + rcv


#*****************************************
# function:  charging_without_map  
# Date :
# Discription:会充电桩
#*****************************************
def charging_without_map(robot, order, arg):
    cmd_content = '"data":{"navigation":{"order":order}}'
    cmd = "{" + cmd_setmotorcomp_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    rcv = robot.connectTCP.recv(1024)
    print 'rcv1:' + rcv



#*****************************************
# function:   set_navigation
# Date :
# Discription:设置当前小胖航位
#*****************************************
def set_navigation(robot, x, y, th):
    cmd_content = '"data":{"navigationset":{"locationx":'+str(x)+',"locationy":'+str(y)+',"locationr":'+str(th)+'}}'
    cmd = "{" + cmd_setnavigation_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
#*****************************************
# function:   camera_take_pic
# Date :
# Discription:执行双目抓拍
#*****************************************
def camera_take_pic(robot,order):
    flag=0
    cmd_content = '"data":{"camera":{"order":"'+order+'"}}'
    cmd = "{" + cmd_camera_header + "," + cmd_content + "}\r\n"
    print 'send:' + cmd
    state=robot.connectTCP.send(cmd)
    print state
    



#*****************************************
# function:   deal_camera_info_recv
# Date :
# Discription:处理双目反馈嘻嘻
#*****************************************
def deal_camera_info_recv(_rcv,arg):
    flag = 1 
    print 'jin ru222---'   
    #判断摄像头 拍照 是否成功
    try:
        if _rcv['state']=='success' :
            print 'success'
        else:
            print 'fail !!'
        if _rcv['move']==0 :
            print 'move ok'
        else:
            print 'nomove !!'
    except:
        pass
    return flag


#*****************************************
# function:   open_infrared_feedback
# Date :
# Discription:打开红外反馈
#*****************************************
def open_infrared_feedback(robot,infrared,arg):
    cmd_content = '"data":{"infrared_status":{"infrared":'+str(infrared)+'}}'
    cmd = "{" + cmd_infrared_data_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    #接收反馈信息
    flag = 0
    if infrared == 1:
        infradata = decode_recv(robot,10,'infrared_status',deal_infrared_recv,arg)
        flag= infradata[0]
        infra_initstate= infradata[1]
        if flag ==-1:
            print 'infrared error'
            logger.error('infrared init error')
            return flag,infra_initstate
        print 'IR over'
        
        return  flag,infra_initstate
    
#*****************************************
# function:   deal_infrared_recv
# Date :
# Discription:处理红外反馈
#*****************************************
def deal_infrared_recv(_rcv, arg):
    flag = 0
    infrastate={}
    #判断红外是否合格
    for _key in _rcv:
        #print _key
        if (_rcv[_key] <= 0) or (_rcv[_key] >= 600):   #300 红外---------------------------------------------------------------------
            flag = -1
            print str(_key) + ":unable"
            
        infrastate[str(_key)]=_rcv[_key]
    if flag==-1:
        logger.error('infrared init error')
        flagd=2
        message= -1,infrastate
        return flagd,message
    flagd=2
    message= flag, infrastate
    return flagd,message




#*****************************************
# function:   ultrasonic_init
# Date :
# Discription:超声波初始化
#*****************************************
def ultrasonic_init(robot,tp,iswrite,num,arg):
    cmd_content = '"data":{"ultrasonic_init":{"type":'+str(tp)+',"iswrite":'+str(iswrite)+',"init":'+str(num)+'}}'
    cmd = "{" + cmd_ultrasonic_init_header + "," + cmd_content + "}\r\n"
    print 'cmd',cmd
    robot.connectTCP.send(cmd)
    flag = 0    
    if tp==1 :
        ultra_initdata = decode_recv(robot,10,'ultrasonicstatus',deal_ultrasonic_init_recv,num)        
        flag= ultra_initdata[0]
        ultra_initstate= ultra_initdata[1]
        print 'flag=',flag,' ultra_initstate=',ultra_initstate
        return flag,ultra_initstate

#*****************************************
# function:   deal_ultrasonic_init_recv
# Date :
# Discription:初始化超声波反馈结果flag
#*****************************************
def deal_ultrasonic_init_recv(_rcv,arg):
    flag = 0
    #判断超声初始化是否完成    
    ultrastate={}
    try:
        cc = _rcv['ultrasonicSum1']*256 + _rcv['ultrasonicSum2']
        
        sumH = _rcv['ultrasonicSum1']
        sumL = _rcv['ultrasonicSum2']
        print 'sumH=',sumH,' sumL=',sumL      

        for i in range(0,8):
            j=7-i
            if (sumL/(2**j))==1:
                ultrastate[str(j)]='Y'
                sumL=sumL-(2**j)
                
            else:
                flag=3
                ultrastate[str(j)]='N'
            print j,'=',ultrastate[str(j)]       
        
        for i in range(0,5):
            j=4-i           
            if (sumH/(2**j))==1:
                ultrastate[str(j+8)]='Y'
                sumH=sumH-(2**j)
            else:
                flag=3               
                ultrastate[str(j+8)]='N'                
            print (j+8),'=',ultrastate[str(j)]
        
    except:       
       logger.error('recv ultrasonic init_info error')
       flagd=2
       message=-1,{}
       return flagd,message
    flagd=2
    message=flag, ultrastate
    return  flagd,message 

#*****************************************
# function:   execute_ultrasonic_init
# Date :
# Discription: 超声波 全部 初始化
#*****************************************
def execute_ultrasonic_init(robot):
    print '+++++ begin ALL ultrasonic init  ++++++'
    init_state=0    
    for i in range(3):
        sonor = 8191        
        ultrasonic_init(robot,0,1,sonor,sonor)
        time.sleep(3)
        init_state=0        
        init_state,ultra_initdata= ultrasonic_init(robot,1,1,sonor,sonor)        
        if init_state == (-1) or init_state == 3:
            print 'init fail ! '
            logger.error('ultrasonic init fail')
            return init_state,ultra_initdata
        else:
            print 'init success'
            break
    time.sleep(1)
    print 'ALL ultrasonic init success'
    print str(ultra_initdata)
    return init_state,ultra_initdata




#*****************************************
# function:   open_ultrasonic_feedback
# Date :
# Discription:打开超声波反馈
#*****************************************
def open_ultrasonic_feedback(robot,feedbacksum,arg):
    cmd_content = '"data":{"feedback_status":{"feedbacksum":'+str(feedbacksum)+'}}'
    cmd = "{" + cmd_ultrasonic_data_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    flag = 0
    if feedbacksum>0 :
        time.sleep(1)
        message = decode_recv(robot,10,'feedback',deal_ultrasonic_feedback_recv,arg)       
        return message
    
#*****************************************
# function:   deal_ultrasonic_feedback_recv
# Date :
# Discription:处理超声波反馈信息
#*****************************************
def deal_ultrasonic_feedback_recv(_rcv,arg):
    flag=0
    #判断超声标定 是否完成
    print 'arg=',arg,'\n'
    ultrastatus={}
    message=()
    try:
        if  _rcv['ultrasonicSum'] == arg[0]:
            print 'feedbackmap='+str(_rcv['feedbackmap'])
            if arg[0]==1:
                num=_rcv['feedbackmap'][0]
                asknum=arg[3]
                print 'num=',num,'asknum=',asknum
                if num == asknum:
                    flagd=2
                    print'num=',num,'data=',_rcv['feedbackmap'][1]
                    print 'type=',type(num)                    
                    if _rcv['feedbackmap'][1]>(arg[1]+arg[2]) or _rcv['feedbackmap'][1]<(arg[1]-arg[2]) :
                        flag=-2                        
                        ultrastatus[1]=str(num),'N'                        
                        logger.error('ultrasonic calibration  distance_info over range')
                    else:
                        ultrastatus[1]=str(num),'Y'
                
                    ultrastatus[0]=_rcv['feedbackmap']
                    print ultrastatus[0]
                    message=flag,ultrastatus
                    return  flagd,message
                else:
                    flagd=3
                return flagd,[]
            elif arg[0]==13:
                flag=2
                message=flag,str(_rcv['feedbackmap'])
                flagd=2
                return  flagd,message
                
    except:        
        logger.error('ultrasonic_feedback message error')
        flagd=3
        message=-1,{}
        return flagd,message


#*****************************************
# function:   excute_ultrasoniccalibration
# Date :
# Discription:执行超声波标定
#*****************************************
def excute_ultrasoniccalibration(robot,arg1,arg2):
    print 'a : top layer ultrasonic calibration'
    i = 0
    flag=0
    dataultra=[]
    dataultraflag=[]
    ultrasonicdata={}
    while i<8:
        print '-------start test ultrasonic.NO= ', (i+1)
        sonor = 1<<i
        ultraflag,ultrainfo=  open_ultrasonic_feedback(robot,sonor,[1,arg1,arg2,i])
        if ultraflag==-1:
            return -1,{}
        elif ultraflag==-2:            
            flag=-2
        else:
            pass
        dataultra.append( ultrainfo[0] )
        dataultraflag.append( ultrainfo[1])
        print 'dataultra=',dataultra
        print 'dataultraflag=',dataultraflag
        time.sleep(1)
        open_ultrasonic_feedback(robot,0,[0])
        print '--------ultrasonic.NO= ', (i+1),' over '
        wheel_move_angle(robot,"left_angle",45)
        time.sleep(4)
        i += 1
    print 'Top ultrasonic test OVER ! '
    wheel_move_angle(robot,"left_angle",90) 
    time.sleep(4)
    print 'b  :bottom layer ultrasonic calibration'
    for i in range(1,6):  
        if i==1:
            j=13
            sonor = 4096
        elif i==2:
            j=11
            sonor = 1024
        elif i==3:
            j=10
            sonor = 512
        elif i==4:
            j=9
            sonor = 256
        elif i==5:
            j=12
            sonor = 2048
        print '-------start test ultrasonic.NO= ',j        
        ultraflag,ultrainfo=  open_ultrasonic_feedback(robot,sonor,[1,arg1,arg2,j-1])
        if ultraflag==-1:
            return -1,{}
        elif ultraflag==-2:
            flag=-2
        else:
            pass
        dataultra.append( ultrainfo[0] )
        dataultraflag.append( ultrainfo[1])
        print 'dataultra=',dataultra
        print 'dataultraflag=',dataultraflag
        print 'flag===',flag
        time.sleep(1)
        open_ultrasonic_feedback(robot,0,[0])
        print '--------ultrasonic over.NO= %d ------'%(j) 
        if i==1:
            wheel_move_angle(robot,"right_angle",60)  
        elif i==2:
            wheel_move_angle(robot,"right_angle",30) 
        elif i==3:
            wheel_move_angle(robot,"right_angle",30)
        elif i==4:
            wheel_move_angle(robot,"right_angle",60) 
        time.sleep(4) 
    print 'c  :bootom layer ultrasonic calibration over '    
    time.sleep(1)
    print 'flag===',flag
    ultrasonicdata[0]=dataultra
    ultrasonicdata[1]=dataultraflag
    print 'zz=',ultrasonicdata
    return  flag,ultrasonicdata

#*****************************************
# function:  camera_calibration_process
# Date :iscription:   双目标定流程26张图
#*****************************************
'''
def camera_calibration_process(robot,rotary_id,delta_angle):    
    #totalNum = 30
    a=0
    b=0
    pic_flag = 1
    state=0
    PicN=1
    j=0
    nomoveNum=0
    failNum=0
    rcv = robot.connectTCP.recv(1024)
    for a in range(0,5):
        for b in range(0,5):
            if j==5 or failNum==5:
                logger.error('camera take pic error')
                return -1
            if nomoveNum==20:
                logger.error('rotary connect error')
                return -1
            try:
                print '\n',"++************ PIC %d ***********++" %(PicN)
                z1=time.time() 
                camera_take_pic(robot,'take_picture')            
                rcv = robot.connectTCP.recv(1024)            
                print 'rcv1',rcv            
                time.sleep(8)
                angle1 = (a-2)*5
                angle2 = (b-2)*5
                print 'rotary angle1=',angle1
                print 'rotary angle2=',angle2
                rotary_controller(rotary_id, angle1, angle2+delta_angle)
                time.sleep(3)
                rcv = robot.connectTCP.recv(1024)            
                json_rcv = json.loads(rcv)            
                print '2rcv',rcv
                print '++********PIC %d state ***********++' %(PicN)
                print json_rcv['data']['camera']['state'].strip()            
                if json_rcv['data']['camera']['state'].strip()  == 'success':                
                    print 'success'
                    if json_rcv['data']['camera']['move']  == 0:
                        nomoveNum+=1                
                        print 'nonMove'
                    else:
                        nomoveNum=0
                        print 'nomoveNum=0'
                    print nomoveNum
                else:
                    failNum += 1
                    print 'Fail'                
                PicN+=1    
                z15=time.time()
                print 'z1t=',z1
                print 'z15t=',z15
                print '++*******************++'
            except:
                print '++********PIC %d state ***********++' %(PicN)
                print 'wrong'
                print '++*******************++'
                j+=1
                print 'j=',j
                time.sleep(1)
    return 0

'''
def camera_calibration_process(robot,rotary_id,delta_angle):    
    totalNum = 37#30-  19.5
    pic_flag = 1
    state=0
    PicN=1
    j=0
    nomoveNum=0
    failNum=0
    rcv = robot.connectTCP.recv(1024)
    while 1:                
        pic_flag = 1 
        if totalNum<12: #15
            break
        if j==5 or failNum==6:
            logger.error('camera take pic error')
            return -1
        if nomoveNum==20:
            logger.error('rotary connect error')
            return -1
        try:
            print '\n',"++************ PIC %d ***********++" %(PicN)
            z1=time.time() 
            camera_take_pic(robot,'take_picture')            
            rcv = robot.connectTCP.recv(1024)            
            print 'rcv1',rcv            
            time.sleep(4)            
            angle1 = (totalNum-25)*2.5
            angle2 = (totalNum-25)*2.5
            print 'rotary angle1=',angle1
            print 'rotary angle2=',angle2
            rotary_controller(rotary_id, angle1, angle2+delta_angle)            
            time.sleep(3)            
            rcv = robot.connectTCP.recv(1024)            
            json_rcv = json.loads(rcv)            
            print '2rcv',rcv
            print '++********PIC %d state ***********++' %(PicN)
            print json_rcv['data']['camera']['state'].strip()            
            if json_rcv['data']['camera']['state'].strip()  == 'success':                
                print 'success'
                if json_rcv['data']['camera']['move']  == 0:
                    nomoveNum+=1                
                    print 'nonMove'
                else:
                    nomoveNum=0
                    print 'nomoveNum=0'
                print nomoveNum
            else:
                failNum += 1
                print 'Fail'                
            
            totalNum -= 1
            PicN+=1
            z15=time.time()
            print 'z1t=',z1
            print 'z15t=',z15
            print '++*******************++'
        except:
            print '++********PIC %d state ***********++' %(PicN)
            print 'wrong'
            print '++*******************++'
            j+=1
            print 'j=',j
            time.sleep(1)
    return 0   

#*****************************************
# function:  camera_calibration_process
# Date :
# Discription:   双目标定流程20张图
#*****************************************
def camera_calibration_process_20(robot,rotary_id,delta_angle):    
    totalNum = 34#30-  19.5
    pic_flag = 1
    state=0
    PicN=1
    j=0
    nomoveNum=0
    failNum=0
    rcv = robot.connectTCP.recv(1024)
    while 1:                
        pic_flag = 1 
        if totalNum<15: #15
            break
        if j==5 or failNum==6:
            logger.error('camera take pic error')
            return -1
        if nomoveNum==20:
            logger.error('rotary connect error')
            return -1
        try:
            print '\n',"++************ PIC %d ***********++" %(PicN)
            z1=time.time() 
            camera_take_pic(robot,'take_picture')            
            rcv = robot.connectTCP.recv(1024)            
            print 'rcv1',rcv            
            time.sleep(4)            
            angle1 = (totalNum-25)*3
            angle2 = (totalNum-25)*3
            print 'rotary angle1=',angle1
            print 'rotary angle2=',angle2
            rotary_controller(rotary_id, angle1, angle2+delta_angle)            
            time.sleep(3)            
            rcv = robot.connectTCP.recv(1024)            
            json_rcv = json.loads(rcv)            
            print '2rcv',rcv
            print '++********PIC %d state ***********++' %(PicN)
            print json_rcv['data']['camera']['state'].strip()            
            if json_rcv['data']['camera']['state'].strip()  == 'success':                
                print 'success'
                if json_rcv['data']['camera']['move']  == 0:
                    nomoveNum+=1                
                    print 'nonMove'
                else:
                    nomoveNum=0
                    print 'nomoveNum=0'
                print nomoveNum
            else:
                failNum += 1
                print 'Fail'                
            
            totalNum -= 1
            PicN+=1
            z15=time.time()
            print 'z1t=',z1
            print 'z15t=',z15
            print '++*******************++'
        except:
            print '++********PIC %d state ***********++' %(PicN)
            print 'wrong'
            print '++*******************++'
            j+=1
            print 'j=',j
            time.sleep(1)
    return 0   
#*****************************************
# function:  camera_deal_data
# Date :
# Discription:   双目处理数据
#*****************************************  
def camera_deal_data(robot):
    camera_take_pic(robot,'save_camera_config')
    try:
        rcv = robot.connectTCP.recv(1024)
        print 'rcv2:' + rcv
        time.sleep(30)
        print '---30S over---'
        flag=0
        i=0
        times=0
        while 1:
            try:
                rcv = robot.connectTCP.recv(10240)
                time.sleep(1)
                print 'rcv3:' + rcv
                json_rcv = json.loads(rcv)                
                print 'camera_json=',json_rcv['data']        
                print 'camera_data= ',json_rcv['data']['camera']['data']
                flag=1
                return flag,json_rcv['data']['camera']['data']                 
            except:
                i+=1
                time.sleep(1)
                print 'i=',i
                if i==30:
                    i=0
                    times+=1
                    if times==2: 
                        logger.error('camera recv info error')
                        flag=-1
                        return flag,{}                                    
    except:
        logger.error('recv robot info error')
        flag=-1
        return flag,{}

#*****************************************
# function:  rotary_controller
# Date :
# Discription:   转台 控制
#***************************************** 
def rotary_controller(rotary_id,angle1,angle2):
    print rotary_id
    import urllib2    
    try:
        if rotary_id[0]=='L':
            print rotary_id[0]
            IP='http://192.168.1.103:10001'
            url = "%s/set_rotary_angle?rotary_id=%s&angle1=%s&angle2=%s"\
            % (IP,str(rotary_id[1]),str(angle1),str(angle2))
        elif rotary_id[0]=='R':
            print rotary_id[0]
            IP='http://192.168.1.102:10001'
            url = "%s/set_rotary_angle?rotary_id=%s&angle1=%s&angle2=%s"\
            % (IP,str(rotary_id[1]),str(angle1),str(angle2))
        #print rotary_id[0:2]
        if rotary_id[0:2] == 'FL' : 
            IP='http://192.168.33.228:80'
            url = "%s/set_rotary_angle?rotary_id=%s&angle1=%s&angle2=%s"\
            % (IP,str(rotary_id),str(angle1), '0')
        elif rotary_id[0:2] == 'FR': 
            IP='http://192.168.33.228:80'
            url = "%s/set_rotary_angle?rotary_id=%s&angle1=%s&angle2=%s"\
            % (IP,str(rotary_id),str(angle1), '0')
        print rotary_id[1]
        
        print url
        page = urllib2.urlopen(url)
        ret = page.read()
        print ret
        flag=2
    except:
        flag=3
        logger.error('rotary connect error')
    return flag
   

#*****************************************
# function:  wheel_camera_calibration
# Date :
# Discription:  行走标定用相机标定 
#*****************************************
def wheel_camera_calibration(camera1,camera2,IP):
    ii=0
    while ii<3:        
        port = 8260
        flagc,con = establish_camera_connect('camera_con',IP,port)
        if flagc==2:            
            break
        else:
            ii+=1       
    if ii==3:
        print u'相机连接失败! 请检查相机的连接!'
        return 3,0 
 
    print u'相机1开始标定 '
    data = camera1
    con.send(data)
    flag =-1
    while True:
        if flag == 1:
            break
        try:
            rcv = con.recv(1024)
            print rcv
            rcv = rcv.replace("'",'"')
            rcv = rcv.strip()  # 去掉  变量前后的 空格                       
            rcv_arr = rcv.split('\r\n')  # 分隔/r/n 前后的内容            
            json_rcv = json.loads(rcv_arr[0]) 
            if json_rcv['type'] == 'take_pic' and json_rcv['data'] == 'success' :
                #time.sleep(2)

                rcv = con.recv(1024)
                print 'e',rcv
                rcv = rcv.replace("'",'"')
                rcv = rcv.strip()  # 去掉  变量前后的 空格                            
                rcv_arr = rcv.split('\r\n')  # 分隔/r/n 前后的内容                
                json_rcv = json.loads(rcv_arr[0])
                if json_rcv['type'] == 'data':
                    print json_rcv['data']                
                    flag = 1
                    break
        except:
            print u'相机1 接收数据失败！'
            return 3,0

    if camera1 != camera2:    
        print '\n',u'相机2开始标定 '
        data = camera2
        con.send(data)
        flag =-1
        while True:
            if flag == 1:
                break
            try:
                rcv = con.recv(1024)
                print rcv
                rcv = rcv.replace("'",'"')
                rcv = rcv.strip()  # 去掉  变量前后的 空格                       
                rcv_arr = rcv.split('\r\n')  # 分隔/r/n 前后的内容            
                json_rcv = json.loads(rcv_arr[0]) 
                if json_rcv['type'] == 'take_pic' and json_rcv['data'] == 'success' :
                    rcv = con.recv(1024)
                    #print rcv
                    rcv = rcv.replace("'",'"')
                    rcv = rcv.strip()  # 去掉  变量前后的 空格                            
                    rcv_arr = rcv.split('\r\n')  # 分隔/r/n 前后的内容                
                    json_rcv = json.loads(rcv_arr[0])
                    if json_rcv['type'] == 'data':
                        print json_rcv['data']                
                        flag = 1
                        break
            except:
                print u'相机2 接收数据失败！'
                return 3,0
       
    con.close()
    
    
#*****************************************
# function:  get_camera_info
# Date :
# Discription:   获取摄像头 拍摄信息（坐标/角度 数据）
#*****************************************
def get_camera_info(cameraID,infotype,IP):
    print IP
    port = 8260
    ii=0
    while ii<2:        
        flagc,con = establish_camera_connect(cameraID,IP,port)        
        if flagc==2:
            data = cameraID            
            con.send(data)            
            break
        else:
            ii+=1        
    if ii==2:
        logger.error('camera soceket connect error')        
        return 3,0    
    flag =1
    ii=0
    while ii<6:
        print 'go'
        if flag == 2:
            break
        try:
            time.sleep(1)
            rcv = con.recv(1024)
            print 'rcv1=',rcv
            rcv = rcv.replace("'",'"')
            rcv = rcv.strip()  # 去掉  变量前后的 空格 
            print rcv           
            rcv_arr = rcv.split('\r\n')  # 分隔/r/n 前后的内容
            print rcv_arr
            for i_num in range(0,len(rcv_arr)):
                print i_num
                json_rcv = json.loads(rcv_arr[i_num])            
                print 'json=',json_rcv['type']
                if json_rcv['type'] == 'take_pic':
                    print json_rcv['data']
                if json_rcv['type'] == 'data':
                    if infotype=='pos':
                        pos_x= json_rcv['data']['x']
                        pos_y= json_rcv['data']['y']
                        print 'x=%.6f , y=%.6f '%(pos_x,pos_y)
                        con.close()
                        flag = 2
                        return flag,pos_y
                    elif infotype=='angle':
                        angle= json_rcv['data']['theta']
                        print 'rcv angle=%.6f '%angle
                        if angle>= -360 and angle<-270:
                            Tangle=angle+360
                        elif angle>= -270  and angle< -90:
                            Tangle=angle+180
                        elif angle<= 360 and angle>270:
                            Tangle=angle-360
                        elif angle<= 270 and angle>90:
                            Tangle=angle-180
                        else:
                            Tangle=-angle
                        print Tangle
                        con.close()
                        flag = 2
                        return flag,Tangle
                    elif infotype=='pos_angle':
                        pos_x= json_rcv['data']['x']
                        pos_y= json_rcv['data']['y']                    
                        angle= json_rcv['data']['theta']
                        print 'x=%.6f , y=%.6f '%(pos_x,pos_y)
                        print 'angle=%.6f '%angle
                        if angle>= -360 and angle<-270:
                            Tangle=angle+360
                        elif angle>= -270  and angle< -90:
                            Tangle=angle+180
                        elif angle<= 360 and angle>270:
                            Tangle=angle-360
                        elif angle<= 270 and angle>90:
                            Tangle=angle-180
                        else:
                            Tangle=-angle
                        print 'Tangle=',Tangle
                        con.close()
                        flag = 2
                        message=pos_x,pos_y,Tangle
                        return flag,message
                    logger.error('request camera formate error')
                    return 3,0 
            ii+=1            
        except:
            ii+=1        
    if ii==6:
        logger.error('camera send info error')
        return 3,0
    
        
#*****************************************
# function:   get_infrared_statusfeed
# Date :
# Discription:
#*****************************************
def get_infrared_statusfeed(robot,isfeed,arg):
    cmd_content = '"data":{"infrared_status_feedback":{"isfeedback":'+str(isfeed)+'}}'
    cmd = "{" + cmd_infra_statusfeedback_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    #接收反馈信息
    flag = 0
    if isfeed == 1:
        flag,infradata = decode_recv(robot,10,'infrared_status',get_infrared_statusdata,arg)
        return  flag,infradata
    
#*****************************************
# function:   get_infrared_statusdata
# Date :
# Discription:
#*****************************************
def get_infrared_statusdata(_rcv, arg):
    flag = 0    
    infrastate={}
    infraflag={}
    infradata={}
    #判断红外是否合格
    for _key in _rcv:
        for infrakey in arg:
            if _key==infrakey:
                if 1782<(arg[infrakey]*8):
                    comparevalue=1782
                else:
                    comparevalue=arg[infrakey]*8
                print 'comparevalue== ',comparevalue
                if (_rcv[_key] <comparevalue):
                    flag=-2
                    infraflag[str(_key)]='N'
                    print str(_key) + ":unable"
                else:
                    infraflag[str(_key)]='Y'                
        infrastate[str(_key)]=_rcv[_key]
    infradata[0]=infrastate
    infradata[1]=infraflag
    flagd=2
    message= flag, infradata
    return flagd,message


#*****************************************
# function:   open_navigation_switch
# Date :
# Discription:
#*****************************************
def open_navigation_switch(robot,switch,arg):
    cmd_content = '"data":{"switch":{"selected":"'+str(switch)+'"}}'
    cmd = "{" + cmd_navigation_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
    #接收反馈信息
    flag = 0
    if switch == "start":
        rcv_y = decode_recv(robot,10,'navigationmessage',deal_navigationmessage_recv,arg)         
        return rcv_y
        
#*****************************************
# function:   deal_navigationmessage_recv
# Date :
# Discription:坐标依据：待验证  zc 
#*****************************************
def deal_navigationmessage_recv(_rcv,arg):
    flag = 0           
    try:       
       print 'X= ',_rcv['locationX'],' ','Y= ',_rcv['locationY'] ,' ','Angle= ',_rcv['locationAngle']
       flagd=2
       message= flag, _rcv['locationX']
       return flagd,message
    except:
       flag = -1
       print 'navigationmessage error'
       logger.error('navigation message error')
       flagd=2
       message=flag,0
       return flagd,message 
                
       
#*****************************************
# function:   switch_obstacle_status
# Date :
# Discription:
#*****************************************      
def switch_obstacle_status(robot,status,arg):
    cmd_content = '"data":{"obstacle_status":{"status":'+str(status)+'}}'
    cmd = "{" + cmd_obstacle_status_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)
   
#*****************************************
# function:   move_to_point
# Date :
# Discription:
#*****************************************
def move_to_point(robot,pointX,pointY,pointAngle):
    cmd_content = '"data":{"fixed_point":{"point_x":'+str(pointX)+',"point_y":'+str(pointY)+',"point_angle":'+str(pointAngle)+'}}'
    cmd = "{" + cmd_movepoint_header + "," + cmd_content + "}\r\n"
    print cmd
    robot.connectTCP.send(cmd)

#*****************************************
# function:   read_wheelroomID
# Date :
# Discription:  读取 数据库 轮间距的 工位ID
#*****************************************    
def read_wheelroomID(robot,arg):
    try:
        sqlHandle = sqlite3.connect(DATABASE_PATH)
        sqlInterface = sqlHandle.cursor()
        sql = 'SELECT wheelspace FROM RobotCalibration WHERE robot_id = "%s" ' % (robot.robot_id)    
        sqlInterface.execute(sql)
        ret = sqlInterface.fetchall()
        if len(ret)==0:
            print 'not find wheelspace data'
            logger.error('not find wheelspace data')
            return -1,{}
        else:
            try:                
                #print 'ret=',ret,'type=',type(ret)                
                rcv=str(ret)
                rcv=rcv.replace('[(u"','',1)        
                rcv=rcv.replace('",)]','',1)
                #print 'rcv=',rcv,'rcv type=',type(rcv)                
                ret=eval(rcv)
                #print 'ret[flag]=',ret['flag']                
                if ret['flag']==2 or ret['flag']==1:                    
                    wheel_roomID=ret['data'][2]
                    print 'wheel_roomID=',wheel_roomID
                    return 2,wheel_roomID
                else:
                    print 'wheelspace not calibration'
                    logger.error('wheelspace not calibration')
                    return 2,'B1'              
            except:
                print 'read wheelspace data error!'
                logger.error('read wheelspace data error!')
                return -1,{}
    except:
        print 'open wheelspace database error!'
        logger.error('open wheelspace database error!')
        return -1,{}

#*****************************************
# function:   read_infrainit_data
# Date :
# Discription:  读取 数据库 红外初始化数据
#*****************************************    
def read_infrainit_data(robot,arg):
    try:
        sqlHandle = sqlite3.connect(DATABASE_PATH)
        sqlInterface = sqlHandle.cursor()
        sql = 'SELECT infra_ultra FROM RobotCalibration WHERE robot_id = "%s" ' % (robot.robot_id)    
        sqlInterface.execute(sql)
        ret = sqlInterface.fetchall()
        if len(ret)==0:
            print 'not find infra_ultra data'
            logger.error('not find infra_ultra data')
            return -1,{}
        else:
            try:                
                print 'ret=',ret,'type=',type(ret)                
                rcv=str(ret)
                rcv=rcv.replace('[(u"','',1)        
                rcv=rcv.replace('",)]','',1)
                print 'rcv=',rcv,'rcv type=',type(rcv)                
                ret=eval(rcv)
                print 'ret[flag]=',ret['flag']                
                if ret['flag']==2 or ret['flag']==3 :
                    if ret['state']['step_state'][1]==2:
                        infrainit_data=ret['data'][0]
                        print 'infrainit_data=',infrainit_data
                        return 2,infrainit_data
                else:
                    print 'infra_ultra not init success'
                    logger.error('infra_ultra not init success')
                    return -1,{}                
            except:
                print 'read infra_ultra data error!'
                logger.error('read infra_ultra data error!')
                return -1,{}
    except:
        print 'open infra_ultra database error!'
        logger.error('open infra_ultra database error!')
        return -1,{}

#*****************************************
# function:   get_roomID
# Date :
# Discription:  读取 工位号 数据库
#*****************************************    
def get_roomID(robot, process):
    try:
        sqlHandle = sqlite3.connect(DATABASE_PATH)
        sqlInterface = sqlHandle.cursor()
        sql = 'SELECT roomID FROM robot_room WHERE robot_id = "%s" ' % (robot.robot_id)    
        sqlInterface.execute(sql)
        ret = sqlInterface.fetchall()
        roomprocess=''
        if len(ret)==0:
            print 'not find the robot roomID'
            logger.error('not find the robot roomID')
            return 3,{}
        else:
            print 'ret[0][0]=',ret[0][0]
            get_roomprocess = ret[0][0][0]
            print 'get_roomprocess=%s'%get_roomprocess
            if   get_roomprocess == 'B' or get_roomprocess == 'X':
                roomprocess='wheelspace'
                print roomprocess 
            elif get_roomprocess == 'L' or get_roomprocess == 'R':
                roomprocess='camera'
                print roomprocess
            elif get_roomprocess == 'D':
                roomprocess='charging'
                print roomprocess
            else:
                print 'the roomID is not correct'
                logger.error('the roomID is not correct')
                return 3,{}
            print "roomID"
            if roomprocess==process:
                print 'the roomID is correct'
                return 2,ret[0][0]
            else:
                print 'the roomID is not current process'
                logger.error('the roomID is not current process')
                return 3,{} 
    except:
        print 'open robot_room database error!'
        logger.error('open robot_room database error!')
        return -1,{}


#*****************************************
# function:   decode_recv
# Date :
# Discription:
#*****************************************
def decode_recv(robot,num,_key,_func, arg):
    flag = 0 #是否检测到有效反馈-标志位
    ret = -1
    for i in range(0,num):#循环接收反馈信息
        if flag == 2:
            break
        time.sleep(1)
        try:
            rcv = robot.connectTCP.recv(10240) #接收反馈信息
            print 'rcv-1:'+rcv
            rcv.replace('}{','}\r\n{')            
            rcv_arr = rcv.split('\r\n')
            print 'split',rcv_arr
            for _rcv in rcv_arr:  #分离反馈信息
                try:
                    print 'split[xx]',_rcv
                    json_rcv = json.loads(_rcv)  #识别json数组
                    print 'json=',json_rcv
                    if _key in json_rcv:                        
                        print 'json[rcv]=',json_rcv[_key]
                        flag,ret = _func(json_rcv[_key],arg)#处理函数
                        print flag
                        print ret
                        print "ultrason__wrong"
                        if flag == 2:                                                       
                            break
                except:
                    print 'decode error1'
        except:
            print 'decode error'
    if i==num-1:
        logger.error('recv robot info error')
        print 'error item=',_key
        if _key=='':
            print '1'
            return -1
        elif _key=='navigationmessage' or _key=='infrared_status':
            print '2'
            return -1,{}
        elif _key=='ultrasonicstatus':
            print '3'
            return -1,{}
        elif _key=='feedback':
            print '4'
            return -1,{}  
    return ret[0],ret[1]


#*****************************************
# function:   excute_ultrasoniccalibration
# Date :
# Discription:
#*****************************************
def excute_Tultrasoniccalibration(robot,arg1,arg2):
    print 'get all ultrasonic calibration data'
    i = 0
    flag=0
    dataultra=[]
    dataultraflag=[]
    ultrasonicdata={}
    tryultrasonic=[]
    		
    sonor = 8191
    ultraflag,ultrainfo=  open_ultrasonic_feedback(robot,sonor,[13,arg1,arg2])
    open_ultrasonic_feedback(robot,0,[0])
    if ultraflag==-1:
        return -1,{}       
       
    flagj,ultrainfo,failInfo = judge_ultrasonic_data(ultrainfo,arg1,arg2)
    dataultra.append( ultrainfo[0] )
    dataultraflag.append( ultrainfo[1])
    print 'dataultra=',dataultra
    print 'dataultraflag=',dataultraflag
    print 'flagj=',flagj
    print 'failinfo=',failInfo
    Num=len(failInfo)
    print 'num=',Num
    if flagj==2:
        flag=2        
    elif flagj==4:
        flag=3
    elif flagj==3:
        Num=len(failInfo)
        for i in range(Num):
            Times=0
            while Times<3:
                sonor = 1<< failInfo[i]       
                ultrasonic_init(robot,0,1,sonor,sonor)
                z1=time.time()
                time.sleep(2)
                z2=time.time()
                print 'z1t=',z1
                print 'z2t=',z2
                ultraflag,ultrainfo= open_ultrasonic_feedback(robot,sonor,[1,arg1,arg2,failInfo[i] ])
                if ultraflag==-1:
                    return -1,{}        
                else:
                    open_ultrasonic_feedback(robot,0,[0])
                tryultrasonic.append(ultrainfo)
                if ultraflag==-2:
                    Times+=1
                    flag=3                    
                else:
                    flag=2                    
                    break                
            
    print 'flag===',flag
    ultrasonicdata[0]=dataultra
    ultrasonicdata[1]=dataultraflag
    ultrasonicdata[2]=tryultrasonic
    print 'zz=',ultrasonicdata
    return  flag,ultrasonicdata



#*****************************************
# function:   judge_ultrasonic_data
# Date :
# Discription:
#*****************************************
def judge_ultrasonic_data(rcv1,distance,internal):
    print 'start judge'
    
    
    rcv=rcv1        
    rcv=rcv.replace('[','{',1)        
    rcv=rcv.replace(']','}',1)
    for j in range(1,14):
        rcv=rcv.replace(',',':',1)        
        rcv=rcv.replace(',',';',1)        
    rcv=rcv.replace(';',',')
    print 'rcv=',rcv
    print 'rcv type=',type(rcv)
    rcv=eval(rcv) 
    print 'transfer_rcv= ',rcv
    
    flag=2
    failInfo=[]
    failNum=0
    ultrastatus={}
    ultrasonicdata=[]
    Trcv=rcv
    ultrastatus[0]=rcv
    
    for i in range(0,13):            
        if Trcv[i]>distance+internal  or Trcv[i]<distance-internal :#---------------------------------------------------------------------------------------------更改现场版本
            ultrastate=str(i),'N'
            failNum+=1
            failInfo.append(i)
            flag=3
            logger.info('ultrasonic NO.%d data out of range' %(i))
        else:
            ultrastate=str(i),'Y'
        ultrasonicdata.append(ultrastate)
    '''
    for i in range(0,13):            
        if Trcv[i]>distance+internal or Trcv[i]<distance-internal :
            ultrastate=str(i),'N'
            failNum+=1
            failInfo.append(i)
            flag=3
            logger.info('ultrasonic NO.%d data out of range' %(i))
        else:
            ultrastate=str(i),'Y'
        ultrasonicdata.append(ultrastate)
    '''
    ultrastatus[1]=ultrasonicdata
    if failNum>5:
        flag=4
        logger.error('over 4 ultrasonic data out of range' )
    return flag,ultrastatus,failInfo


#*****************************************
# function:  cameracomputer_close
# Date :
# Discription:  关闭摄像头服务器主机 
#*****************************************
def cameracomputer_close(command,IP):
    ii=0
    while ii<3:        
        port = 8260
        flagc,con = establish_camera_connect('camera_con',IP,port)
        if flagc==2:            
            break
        else:
            ii+=1       
    if ii==3:
        print u'%s连接失败! 请手动切换关机!'%IP
        return 3,0 
 
    print u'%s连接成功'%IP
    data = command
    con.send(data)
    flag =-1
    while True:
        if flag == 1:
            break
        try:
            rcv = con.recv(1024)
            print rcv
            if rcv=="closed":
                flag=1
        except:
            print u'%关机失败! 请手动切换关机!'%IP
            return 3,0       
    con.close()
'''
while 1:
    
    rotary_controller('001',-20,-30)    
    time.sleep(10)
print 'ok'
'''

#*****************************************
# function:   take_rotate_platform_position
# Date :
# Discription:双目识别转台位置
#*****************************************
def take_rotate_platform_position(robot,order):
    flag=0
    cmd_content = '"data":{"camera":{"order":"'+order+'"}}'
    cmd = "{" + cmd_camera_header + "," + cmd_content + "}\r\n"
    print cmd
    state=robot.connectTCP.send(cmd)
    print state

#*****************************************
# function: get_rotate_platform_postion
# Date :
# Discription:   获取转台位置
#*****************************************  
def get_rotate_platform_position(robot):
    take_rotate_platform_position(robot,'get_rotate_platform_position')
    try:
        rcv = robot.connectTCP.recv(1024)
        print 'rcv2:' + rcv
        time.sleep(3)
        print '---30S over---'
        flag=0
        i=0
        times=0
        while 1:
            try:
                rcv = robot.connectTCP.recv(10240)
                time.sleep(1)
                print 'rcv3:' + rcv
                json_rcv = json.loads(rcv)                
                print 'camera_json=',json_rcv['data']        
                print 'camera_data= ',json_rcv['data']['camera']['data']
                flag=1
                return flag,json_rcv['data']['camera']['data']                 
            except:
                i+=1
                time.sleep(1)
                print 'i=',i
                if i==30:
                    i=0
                    times+=1
                    if times==2: 
                        logger.error('camera recv rotate platform position info error')
                        flag=-1
                        return flag,{}                                    
    except:
        logger.error('recv robot info error')
        flag=-1
        return flag,{}


#*****************************************
# function:   take_check_camera_params
# Date :
# Discription:进行双目检验
#*****************************************
def take_check_camera_params(robot,order):
    flag=0
    cmd_content = '"data":{"camera":{"order":"'+order+'"}}'
    cmd = "{" + cmd_camera_header + "," + cmd_content + "}\r\n"
    print cmd
    state=robot.connectTCP.send(cmd)
    print state

#*****************************************
# function: get_check_camera_params
# Date :
# Discription:   获取双目检验结果
#*****************************************  
def get_check_camera_params(robot):
    take_check_camera_params(robot,order)(robot,'check_camera_params')
    try:
        rcv = robot.connectTCP.recv(1024)
        print 'rcv2:' + rcv
        time.sleep(3)
        print '---30S over---'
        flag=0
        i=0
        times=0
        while 1:
            try:
                rcv = robot.connectTCP.recv(10240)
                time.sleep(1)
                print 'rcv3:' + rcv
                json_rcv = json.loads(rcv)                
                print 'camera_json=',json_rcv['data']        
                print 'camera_data= ',json_rcv['data']['camera']['result']
                flag=1
                return flag,json_rcv['data']['camera']['result']                 
            except:
                i+=1
                time.sleep(1)
                print 'i=',i
                if i==30:
                    i=0
                    times+=1
                    if times==2: 
                        logger.error('camera recv rotate platform position info error')
                        flag=-1
                        return flag,{}                                    
    except:
        logger.error('recv robot info error')
        flag=-1
        return flag,{}


#*****************************************
# function:   take_check_location_picture
# Date :
# Discription:   本地图片检测
#*****************************************
def take_check_location_picture(robot,order):
    flag=0
    cmd_content = '"data":{"camera":{"order":"'+order+'"}}'
    cmd = "{" + cmd_camera_header + "," + cmd_content + "}\r\n"
    print cmd
    state=robot.connectTCP.send(cmd)
    print state

#*****************************************
# function: get_check_location_picture
# Date :
# Discription:   返回本地图片检测结果
#*****************************************  
def get_check_location_picture(robot):
    take_check_location_picture(robot,'check_location_picture')
    try:
        rcv = robot.connectTCP.recv(1024)
        print 'rcv2:' + rcv
        time.sleep(3)
        print '---30S over---'
        flag=0
        i=0
        times=0
        while 1:
            try:
                rcv = robot.connectTCP.recv(10240)
                time.sleep(1)
                print 'rcv3:' + rcv
                json_rcv = json.loads(rcv)                
                print 'camera_json=',json_rcv['data']        
                print 'camera_data= ',json_rcv['data']['camera']['result']
                flag=1
                return flag,json_rcv['data']['camera']['result']                 
            except:
                i+=1
                time.sleep(1)
                print 'i=',i
                if i==30:
                    i=0
                    times+=1
                    if times==2: 
                        logger.error('camera recv check location picture info error')
                        flag=-1
                        return flag,{}                                    
    except:
        logger.error('recv robot info error')
        flag=-1
        return flag,{}
#liyao 首次双目标定
#*****************************************
# function:   get_json_state
# Date :
# Discription:   返回json命令结果
# 2017年1月13日 liyao
#*****************************************
def get_json_state(robot,f_tag,s_tag,t_tag):
#     ret = robot.connectTCP.recv(1024)
#     print ret;
#     try:
#         json_rcv = json.loads(ret)
#     except:
#         print 'get_json_state json解析失败\n'
#         return 0
#     if json_rcv[f_tag][s_tag][t_tag].strip()  == 'success':
#         return 1
#     else:
#         return 0
    for i in range(10):
        try:
            rcv = robot.connectTCP.recv(10240) #接收反馈信息
            print 'rcv-1:'+rcv
            rcv.replace('}{','}\r\n{')            
            rcv_arr = rcv.split('\r\n')
            #print 'split',rcv_arr
            for _rcv in rcv_arr:  #分离反馈信息
                try:
                    #print 'split[xx]',_rcv
                    json_rcv = json.loads(_rcv)  #识别json数组
                    if json_rcv[f_tag][s_tag][t_tag].strip()  == 'success':
                        return 1
                    else:
                        sleep(1)
                        continue  
                except:
                    print ''
        except: 
            sleep(1)
            continue   
    return 0
#*****************************************
# function:   set_picn_location
# Date :
# Discription:   发送图片序号并获取转台偏移位置
# 2017年1月13日 liyao
#*****************************************
def set_picn_location(robot, pic_seq): 
    cmd_content = '"data":{"camera":{"order":"fixed_plate","picture_id":'+str(pic_seq)+'}}'
    cmd = "{" + cmd_camera_header + "," + cmd_content + "}\r\n"
    print 'send:' + cmd
    state=robot.connectTCP.send(cmd)
    return state        
#*****************************************
# function:   get_slipway_location
# Date :
# Discription:   获取滑台偏移位置
# 2017年1月13日 liyao
#*****************************************
def get_slipway_location(robot):
    for i in range(10):
        rcv = robot.connectTCP.recv(1024)
        print 'recv-2'+rcv;
        try:  
            rcv.replace('}{','}\r\n{')            
            rcv_arr = rcv.split('\r\n')
            #print 'split',rcv_arr
            for _rcv in rcv_arr:  #分离反馈信息
                try:
                    #print 'split[xx]',_rcv
                    json_rcv = json.loads(_rcv)  #识别json数组
                    if json_rcv['data']['camera']['state'].strip()  == 'success':
                        try:
                            offset = json_rcv['data']['camera']['instance']
                            print '滑台修正位置'+str(offset)+'\n'
                            return offset
                        except:
                            print ''
                    elif json_rcv['data']['camera']['state'].strip()  == 'fail':
                        return 'fail'
                except:
                    print ''
            sleep(1)
            continue
        except:
            sleep(1)
            continue   
    return 'fail'       

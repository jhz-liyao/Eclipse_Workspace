# -*- coding: utf-8 -*-
#==============================================================================
# Group:   JHZ-Robot
# Project: Motor Calibration
# File :   protocol.py
# Date :   2016-01-07
# Discription :
#          server2robot protocol.
#==============================================================================
from mylog import*
import ConfigParser
from app_config import ROBOT_PATH

def read_configfile(option):
    conf = ConfigParser.ConfigParser()
    conf.read(ROBOT_PATH+"\para.conf")

    #获取所有的section
    #sections = conf.sections()
    #print sections

    # 获取指定的section， 指定的option的值
    
    #--- 行走控制配置参数 ---#
    if option=='move':
        try:
            move_d1 = conf.getfloat("move", "move_d1")
            print move_d1    
            move_d2 = conf.getfloat("move", "move_d2")
            print move_d2
            move_wheelbase = conf.getfloat("move", "move_wheelbase")
            print move_wheelbase
            move_d3 = conf.getfloat("move", "move_d3")
            print move_d3
            flag=2
            message= move_d1, move_d2, move_wheelbase, move_d3
        except:
            logger.error('the para.conf of move exist error')
            flag=3
            message=0,0,0,0
        return flag,message

    #--- 航位控制配置参数 ---#    
    if option=='odometer':
        try:
            odometer_d1 = conf.getfloat("odometer", "odometer_d1")
            print odometer_d1    
            odometer_wheelbase = conf.getfloat("odometer", "odometer_wheelbase")
            print odometer_wheelbase
            flag=2
            message= odometer_d1, odometer_wheelbase
        except:
            logger.error('the para.conf of odometer exist error')
            flag=3
            message=0,0
        return flag,message

    #--- 轮间距配置参数 ---#
    if option=='wheelspace':
        try:
            wheelspace_n = conf.getfloat("wheelspace", "wheelspace_n")
            print wheelspace_n    
            odometer_wheelbase = conf.getfloat("wheelspace", "wheelspace_base")
            print odometer_wheelbase
            wheelspace_H = conf.getfloat("wheelspace", "wheelspace_H")
            print wheelspace_H
            wheelspace_L = conf.getfloat("wheelspace", "wheelspace_L")
            print wheelspace_L
            wheelspace_theta = conf.getfloat("wheelspace", "wheelspace_theta")
            print wheelspace_theta
            flag=2
            message= wheelspace_n, odometer_wheelbase,wheelspace_H,wheelspace_L,wheelspace_theta
        except:
            logger.error('the para.conf of wheelspace exist error')
            flag=3
            message=0,0,0,0,0
        return flag,message

    #--- 红外+超声波初始化 配置参数 ---#    
    if option=='init_infra_ultrasonic':        
        try:            
            init_ultrasonic_Ld = conf.getfloat("init_infra_ultrasonic", "init_ultrasonic_Ld")            
            print init_ultrasonic_Ld    
            init_ultrasonic_Lin = conf.getfloat("init_infra_ultrasonic", "init_ultrasonic_Lin")
            print init_ultrasonic_Lin
            flag=2
            message= init_ultrasonic_Ld, init_ultrasonic_Lin
        except:
            logger.error('the para.conf of init_infra_ultrasonic exist error')
            flag=3            
            message=0,0
        return flag,message

    #--- 双目配置参数 ---#
    if option=='camera':
        try:
            camera_L1  = conf.getfloat("camera", "camera_L1")
            print camera_L1    
            camera_L2  = conf.getfloat("camera", "camera_L2")
            print camera_L2
            camera_L3  = conf.getfloat("camera", "camera_L3")
            print camera_L3    
            camera_L4  = conf.getfloat("camera", "camera_L4")
            print camera_L4
            camera_L5  = conf.getfloat("camera", "camera_L5")
            print camera_L5    
            camera_L6  = conf.getfloat("camera", "camera_L6")
            print camera_L6
            camera_R1  = conf.getfloat("camera", "camera_R1")
            print camera_R1    
            camera_R2  = conf.getfloat("camera", "camera_R2")
            print camera_R2
            camera_R3  = conf.getfloat("camera", "camera_R3")
            print camera_R3    
            camera_R4  = conf.getfloat("camera", "camera_R4")
            print camera_R4
            camera_R5  = conf.getfloat("camera", "camera_R5")
            print camera_R5    
            camera_R6  = conf.getfloat("camera", "camera_R6")
            print camera_R6            
            flag=2
            message= camera_L1,camera_L2,camera_L3,camera_L4,camera_L5,camera_L6,\
                     camera_R1,camera_R2,camera_R3,camera_R4,camera_R5,camera_R6 
        except:
            logger.error('the para.conf of camera exist error')
            flag=3
            message=0,0,0,0,0
        return flag,message


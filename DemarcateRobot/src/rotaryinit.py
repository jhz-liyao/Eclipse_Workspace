# -*- coding: utf-8 -*-
from protocol import *
#*****************************************
# function:  rotary_init
# Date :
# Discription:   执行各个标定过程
#*****************************************
def rotary_init_LR(LR,angle):
    for i in range(1,7):
        r_id = LR+str(i)
        #rotary_controller(r_id,45,45)
        rotary_controller(r_id,angle,angle)
        print r_id
        
def rotary_init(arg):
    from time import *
    print 'rotary_init start'
    angle=45
    rotary_init_LR('L',angle)
    rotary_init_LR('R',angle)
    sleep(20)
    angle=-45
    rotary_init_LR('L',angle)
    rotary_init_LR('R',angle)
    sleep(20)
    angle=0
    rotary_init_LR('L',angle)
    rotary_init_LR('R',angle)
    print 'rotary_init over'



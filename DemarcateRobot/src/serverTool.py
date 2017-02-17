#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
PROCESS_ITEM = {'camera_first','move','odometer','wheelspace','infra_ultra',\
                'camera','move_check','wheelspace_check',}
def process_parse(robot_cmd):
    item = ''
    if robot_cmd == 0:
        item = 'camera_first'
    if robot_cmd == 1:
        item = 'move'
    if robot_cmd == 2:
        item = 'odometer'    
    if robot_cmd == 3:
        item = 'wheelspace'
    if robot_cmd == 4:
        item = 'infra_ultra'
    if robot_cmd == 5:
        item = 'camera'
    if robot_cmd == 11:
        item = 'move_check'
    if robot_cmd == 12:
        item = 'wheelspace_check'  
    if robot_cmd == 100:
        item = 'troubleshoot'
    return item

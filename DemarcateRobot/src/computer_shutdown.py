#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
from sys_env import *
from protocol import *
import time
import os
    
#--------------------相机标定主函数-----------------------------
if __name__ == '__main__':
    
    print u'---进入相机标定流程---'
    i=0
    while i==0:
        N=raw_input(unicode('请输入s关闭23456电脑:','utf-8').encode('gbk'))        
     
        if N=='s' or N=='S':
            cameracomputer_close('shutdown','192.168.2.110')
            cameracomputer_close('shutdown','192.168.3.111')
            cameracomputer_close('shutdown','192.168.4.112')
            cameracomputer_close('shutdown','192.168.5.113')
            cameracomputer_close('shutdown','192.168.6.114')
            #import os
            #os.system("cmd.exe /k shutdown /m \\192.168.1.103 -s")
            #os.system('cmd.exe /k ping 192.168.1.103')
            #command = 'cmd.exe /k shutdown -m \\192.168.1.103 -s -t 30'
            #command = 'shutdown /m \\192.168.1.103 -s -t 30'
            #os.system(command)
            print u'  关机完成! '

            import os
            os.system('start F:\pyserver\close_home_computer.bat')

        '''
        elif N=='h':
            import os
            os.system('start close_home_Computer.bat')
            #使用下边命令不能识别IP主机
            os.system('shutdown /m \\192.168.1.103 -s -t 30')
        '''    

        '''
        elif N=='r':
            wheel_camera_calibration('restart','restart','192.168.2.110')
            #wheel_camera_calibration('restart','restart','192.168.3.111')
            #wheel_camera_calibration('restart','restart','192.168.4.112')
            #wheel_camera_calibration('restart','restart','192.168.5.113')
            #wheel_camera_calibration('restart','restart','192.168.6.114')
            #import os
            #os.system("cmd.exe /k shutdown /m \\192.168.1.103 -s")
            #os.system('cmd.exe /k ping 192.168.1.103')
            #command = 'cmd.exe /k shutdown -m \\192.168.1.103 -s -t 30'
            #command = 'shutdown /m \\192.168.1.103 -s -t 30'
            #os.system(command)
            print u'  重启完成! '
        else:
            print u'  输入相机编号错误! 请重新输入!'
        '''
        i+=1
    print u'---close!--- '
    time.sleep(10)


     


#!C:\Python27\python.exe
# -*- coding: utf-8 -*-
from protocol import *
from sys_env import *
from time import *
#--------------------相机标定主函数-----------------------------
if __name__ == '__main__':    
    print u'---进入相机标定流程---'
    i=0
    n5=0
    n6=0
    n7=0
    n8=0
    n11=0
    n12=0
    n=0
    while i<100:
        N=raw_input(unicode('请输入需要标定的相机编号:','utf-8').encode('gbk'))        
        if N=='1':
            #-----------行走控制标定相机标定-----------
            #wheel_camera_calibration('100263780','100399800','192.168.1.110')
            #print u'  相机1行走 标定完成! '
            flag_cam1,theta_start1=get_camera_info('00263780','angle','192.168.1.110')
            #flag_cam2,theta_start2=get_camera_info('00399800','angle','192.168.1.110')
            #if flag_cam1 != 3 :
            print u'  相机1通讯完成! ',flag_cam1
            #if flag_cam2!=3:
            #print u'  相机2通讯完成! ',flag_cam2
        elif N=='2':
            #----------行走航位标定相机标定----------------
            #wheel_camera_calibration('100366817','100408370','192.168.1.111')
            #print u'  相机2航位 标定完成! '
            flag_cam1,theta_start1=get_camera_info('00366817','angle','192.168.1.111')
            #flag_cam2,theta_start2=get_camera_info('00408370','pos_angle','192.168.1.111')
            if flag_cam1!=3:
                print u'  相机3通讯完成! '
            #if flag_cam2!=3:
            #    print u'  相机4通讯完成! '
        elif N=='3':
            #----------轮间距标定相机标定----------------
            #wheel_camera_calibration('100289713','100289713','192.168.1.112')
            #print u'  相机3轮间距 标定完成! '
            #while 1:
                #flag_cam1,theta_start1=get_camera_info('00289713','angle','192.168.1.112')
            flag_cam2,pos_angle_start2=get_camera_info('00270925','pos_angle','192.168.1.112')
                #print "get_camera_info "
            print pos_angle_start2
                #if flag_cam1!=3:
                 #  print u'  相机5通讯完成! '
                #else:
                 #   n5+=1
            if flag_cam2!=3:
                print u'  相机6通讯完成! '
                #else:
                #    n6+=1
                #n+=1
                #print n
                #print n5
            print n6
        elif N=='4':
            #----------L双目标定相机标定----------------
            #wheel_camera_calibration('100453594','100453594','192.168.1.112')
            #print u'  相机4双目  标定完成! '
            '''
            while 1:
                flag_cam1,theta_start1=get_camera_info('00453594','angle','192.168.1.113')
                if flag_cam1!=3:
                    print u'  相机7通讯完成! '
                else:
                    n7+=1
                n+=1
                print n
                print n7
                sleep(1)
            '''
            while 1:
                flag_cam2,theta_start2=get_camera_info('00323320','angle','192.168.1.113')
                if flag_cam2!=3:
                    print u'  相机8通讯完成! '
                else:
                    n8+=1
                n+=1
                print n
                print n8
                sleep(1)
            flag_cam2,theta_start2=get_camera_info('00323320','angle','192.168.1.113')
            if flag_cam2!=3:
                print u'  相机8通讯完成! '
            '''
            sleep(3)
            while 1:
                flag_cam3,theta_start3=get_camera_info('00327878','angle','192.168.1.113')
                if flag_cam3!=3:
                    print u'  相机9通讯完成! '
                sleep(5)
            flag_cam4,theta_start4=get_camera_info('00402546','angle','192.168.1.113')
            if flag_cam4!=3:
                print u'  相机10通讯完成! '
            '''
        elif N=='5':
            #----------L双目标定相机标定----------------
            #wheel_camera_calibration('100323320','100323320','192.168.1.112')
            #print u'  相机5双目  标定完成! '
            while 1:
                flag_cam1,theta_start1=get_camera_info('00361432','angle','192.168.1.114')
                flag_cam2,theta_start2=get_camera_info('00384058','angle','192.168.1.114')
                if flag_cam1!=3:
                    print u'  相机11通讯完成! '
                else:
                    n11+=1
                if flag_cam2!=3:
                    print u'  相机12通讯完成! '
                else:
                    n12+=1
                n+=1
                print n
                print n11
                print n12
        else:
            print u'  输入相机编号错误! 请重新输入!'
        i+=1
    print u'---相机标定结束!--- '
    sleep(3)


     


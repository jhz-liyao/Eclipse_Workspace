# -*- coding: utf-8 -*-
#==============================================================================
# Group:   JHZ-Robot
# Project: Motor Calibration
# File :   protocol.py
# Date :   2016-01-07
# Discription :
#          server2robot protocol.
#==============================================================================

import logging

# 创建一个logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] [robotID:%(threadName)s] [%(levelname)s :%(message)s]',
                    #datefmt='%a,%d %b %Y %H:%M:%S',
                    filename='mylog.log',
                    filemode='a+')
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
#fh = logging.FileHandler('mylog.log')
#fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#ch.setFormatter(formatter)
# 给logger添加handler
#logger.addHandler(fh)
logger.addHandler(ch)
# 记录一条日志
#logger.info('qqq12foorbee344r')


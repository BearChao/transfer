#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/8 下午6:49
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : util.py
# @Software: PyCharm
import psutil
import time
import socket
import fcntl
import struct


def get_memory():
    return psutil.swap_memory().percent

def get_bootTime():
    t = time.localtime(psutil.boot_time())
    return time.strftime('%Y-%m-%d %H:%M:%S',t)

def get_disk():
    dis_syl = psutil.disk_usage('/').used / float(psutil.disk_usage('/').total) * 100
    return "%.2f" % dis_syl

#! /usr/bin/python

'''
CentOS 6.2 + Python 2.6
'''
def getIpList():
    '''
    >>> print(getIpList())
    :return:
    '''
    import os
    ipList = []
    var = os.popen('ifconfig').read().split("\n\n")
    for item in var:
            #print item
            symble1 = "inet addr:"
            pos1 = item.find(symble1)
            if pos1 >= 0:
                    #print "find it : ",pos1
                    tmp1 = item[pos1+len(symble1):]
                    ipList.append(tmp1[:tmp1.find(" ")])
    return ipList

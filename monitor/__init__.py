#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/26 下午3:25
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : __init__.py.py
# @Software: PyCharm
from collections import OrderedDict


def cpuinfo():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    loadavg['nr']=con[3]
    loadavg['last_pid']=con[4]
    return round(float(loadavg['lavg_15'])*100,2)

def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()
    with open('/proc/meminfo') as f: #proc/
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    total = float(meminfo['MemTotal'][:-3])/1024
    free = float(meminfo['MemFree'][:-3])/1024
    percent = (total-free)/total*100
    return round(percent,2),round(free,2)







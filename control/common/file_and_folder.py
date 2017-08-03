#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/29 下午2:55
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : file_and_folder.py
# @Software: PyCharm
import datetime
import pickle

from flask import current_app

from conf.timeout import SYSOATHTIME
from control.common import LOGS
import os

def mkdir(path):
    # 取路径
    path = os.path.split(path)[0]

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        LOGS.debug('创建文件夹:'+path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

def allow():
    if os.path.isfile('conf/auth'):
        return True
    else:
        return check_date()

def notice():
    if os.path.isfile('conf/auth'):
        return None
    else:
        endtime = get_date_()
        if endtime is None:
            return '系统未激活，将停止服务：未发现激活时间信息'
        if (endtime-datetime.datetime.now()).days <= 10:
            return '系统未激活，将从以下日期开始停止服务：'+endtime.strftime('%Y-%m-%d')
        else:
            return None

def check_date():
    t = SYSOATHTIME
    try:
        boost = pickle.load(open('conf/boost','rb'))
        time = datetime.datetime.now()
        if (time-boost).days > t:
            return False
        else:
            return True
    except Exception as e:
        print('检查日期出错：'+str(e))
        return False

def get_date_():
    t = SYSOATHTIME
    if not t:
        return None
    boost = pickle.load(open('conf/boost', 'rb'))
    time = datetime.datetime.now()
    time = boost + datetime.timedelta(days =t)
    return time


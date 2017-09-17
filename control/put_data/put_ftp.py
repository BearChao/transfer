#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 下午3:42
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : put_ftp.py
# @Software: PyCharm
from control.common import LOGR
from control.get_data.get_ftp import MyFTP


def putFTP(task,file):
    try:
        conn = MyFTP(task.target, int(task.port), str(task.finger))
        conn.Login(task.username, task.password)
        path = file[5:]
        conn.UpLoadFile(file,path)
        return True
    except Exception as e:
        LOGR.error('FTP上传错误：'+str(e))
        return False

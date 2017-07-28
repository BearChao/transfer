#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 下午3:42
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : put_ftp.py
# @Software: PyCharm
from control.get_data.get_ftp import FTPSync


def putFTP(task,file):
    conn = FTPSync(task.target, task.port, str(task.finger))
    conn.login(task.username, task.password)
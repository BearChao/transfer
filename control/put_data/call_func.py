#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/3 下午11:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : call_func.py
# @Software: PyCharm
from control.task.task import DATATYPE


def putData(task):
    type = task.dataType
    if type == DATATYPE.FTP.value:
        return putFTP(task)
        pass
    elif type == DATATYPE.MYSQL.value:
        print('2')
        return putMySQL(task)
        pass
    elif type == DATATYPE.FILE.value:
        return putFile(task)
    elif type == DATATYPE.ORACLE.value:
        pass
    elif type == DATATYPE.WEBDAV.value:
        pass
    else:
        return []
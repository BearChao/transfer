#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/3 下午11:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : call_func.py
# @Software: PyCharm
from control.put_data.put_ftp import putFTP
from control.put_data.put_mysql import putMySQL
from control.put_data.put_smb import putSMB
from control.task.task import DATATYPE


def putData(task,file):
    type = task.dataType
    if type == DATATYPE.FTP.value:
        return putFTP(task,file)
        pass
    elif type == DATATYPE.MYSQL.value:
        return putMySQL(task,file)
        pass
    elif type == DATATYPE.FILE.value:
        return putFile(task,file)
    elif type == DATATYPE.ORACLE.value:
        pass
    elif type == DATATYPE.WEBDAV.value:
        pass
    elif type == DATATYPE.SMB.value:
        return putSMB(task,file)
    else:
        return False
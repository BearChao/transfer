#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午8:35
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : call_func.py
# @Software: PyCharm
from control.get_data.get_file import getFile
from control.get_data.get_ftp import getFTP
from control.task.task import DATATYPE
from control.get_data.get_mysql import getMySQL

def getDataFile(task):
    '''
    根据传递的task选择对应的服务，然后将获取的数据按照规则保存到本地
    :return:本地文件列表list，已经修改名字，保持原有目录结构
    '''
    type = task.dataType
    if type == DATATYPE.FTP.value:
        return getFTP(task)
    elif type == DATATYPE.MYSQL.value:
        return getMySQL(task)
    elif type == DATATYPE.FILE.value:
        return getFile(task)
    elif type == DATATYPE.ORACLE.value:
        pass
    elif type == DATATYPE.WEBDAV.value:
        pass
    elif type == DATATYPE.SMB.value:
        pass
    else:
        return []


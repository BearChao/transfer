#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午8:35
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : call_func.py
# @Software: PyCharm
from get_data import get_file
from model.Config import DATATYPE

from control.get_data import get_ftp


def getDataFile(configItem):
    '''
    根据传递的config item选择对应的服务，然后将获取的数据按照规则保存到本地
    :return:本地文件列表list，已经修改名字，保持原有目录结构
    '''
    files = []
    type = configItem.dataType
    if type == DATATYPE.FTP.value:
        return get_ftp.getFTP(configItem)
        pass
    elif type == DATATYPE.MYSQL.value:
        pass
    elif type == DATATYPE.FILE.value:
        return get_file.getFile(configItem)
    elif type == DATATYPE.ORACLE.value:
        pass
    elif type == DATATYPE.WEBDAV.value:
        pass


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午8:35
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : call_func.py
# @Software: PyCharm
from get_data import get_file
from model.Config import DATATYPE


def getDataFile(configItem):
    '''
    根据传递的config item选择对应的服务，然后将获取的数据按照规则保存到本地
    :return:文件列表list
    '''
    files = []
    type = configItem.dataType
    if type == DATATYPE.FTP.value:
        pass
    elif type == DATATYPE.MYSQL.value:
        pass
    elif type == DATATYPE.FILE.value:
        return get_file.getFile(configItem)
    elif type == DATATYPE.ORACLE.value:
        pass
    elif type == DATATYPE.WEBDAV.value:
        pass


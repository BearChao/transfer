#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午10:22
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : task.py
# @Software: PyCharm
from enum import Enum
import time


class DATATYPE(Enum):
    FILE = "file"
    FTP = "ftp"
    WEBDAV = "webDav"
    #>10则为数据库类型
    MYSQL = "mysql"
    ORACLE = "oracle"
    #todo 枚举中添加其他类型

def get_finger():
    return int(time.strftime("%Y%m%d%H%M%S", time.localtime()))


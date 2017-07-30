#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/30 上午11:52
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : put_file.py
# @Software: PyCharm
import os
import shutil

from control.common import LOGR


def putFile(task,file):
    try:
        path = task.dir.strip("/")
        path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        shutil.copy(file, path)
        return True
    except Exception as e:
        LOGR.error('文件复制错误：'+str(e))
        return False
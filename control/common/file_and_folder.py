#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/29 下午2:55
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : file_and_folder.py
# @Software: PyCharm

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
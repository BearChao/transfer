#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午6:42
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : file_sender.py
# @Software: PyCharm

"""
负责执行发送文件模块
"""
import os
import subprocess
import logging


def sendFile(fileName):
    #传入文件名，将文件发送到接收端
    #文件名允许为目录形式，接收端接收到的文件也会存入对应目录位置
    command = ["./transfer_file","-s"]
    command.append('temp/'+fileName)
    result = subprocess.call(command)
    if result == 0:
        logging.log(logging.INFO,'文件发送完毕：'+fileName)
        return True
    else:
        return False

def rename(files,id):
    '''
    批量重命名文件
    :param files: 文件路径list
    :param id: 任务id
    :return:
    '''
    subfix = '.'+str(id)
    for f in files:
        os.rename(f,f+subfix)
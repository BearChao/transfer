#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:13
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_sender.py
# @Software: PyCharm
import sys

from common import LOGS
from common.file_sender import sendFile
from get_data.call_func import getDataFile
from model.Config import Config


def run(id):
    #解析任务
    conf = Config()
    conf.load()
    task = conf.getConfigItem(id)
    if task is None:
        LOGS.error('找不到对应任务：'+str(id))
        exit(-1)
    LOGS.info('开始任务：' + str(id)+":"+task.name)

    #todo 获取文件
    files = getDataFile(task)

    #发送文件
    for f in files:
        print("send:"+f)
    #sendFile("ls")
    LOGS.info('文件发送完成')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        id = int(sys.argv[1])
        run(id)
    else:
        LOGS.error('参数错误,未提供任务id')
        exit(-1)
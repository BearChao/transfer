#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:13
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_sender.py
# @Software: PyCharm
import sys

from app.models import Task, db
from control.common import LOGS
from control.common.file_sender import sendFile
from control.get_data.call_func import getDataFile


def run(id):
    #解析任务
    db.connect()
    task = Task.get(Task.finger == id)
    if task is None:
        LOGS.error('找不到对应任务：'+str(id))
        exit(-1)
    else:
        task = task[0]
    db.close()
    LOGS.info('开始任务：' + str(id)+":"+task.name)

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
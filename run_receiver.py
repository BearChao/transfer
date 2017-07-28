#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:13
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_sender.py
# @Software: PyCharm
import os
import sys

from app.models import Task, db
from control.common import LOGS
from control.common.file_sender import sendFile
from control.get_data.call_func import getDataFile
from control.put_data.call_func import putData


def run(file):
    list = file.split('.')
    id = int(list[-1])
    new_file = list[0]+'.'+list[1]
    os.rename(file,new_file)
    #解析任务
    db.connect()
    task = Task.get(Task.finger == id)
    if task is None:
        LOGS.error('找不到对应任务：'+str(id))
        exit(-1)
    #增加运行次数
    task.count = task.count + 1
    task.save()
    db.close()
    LOGS.info('开始任务：' + str(id)+":"+task.name)
    result = putData(task,new_file)
    if result:
        LOGS.info('任务执行完成：'+file)
    else:
        LOGS.info('任务执行失败：'+file)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        run(file)
    else:
        LOGS.error('参数错误,未提供任务id')
        exit(-1)
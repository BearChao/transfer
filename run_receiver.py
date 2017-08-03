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
from control.common import LOGR
from control.put_data.call_func import putData


def run(file):
    list = file.split('.')
    id = int(list[-1])
    file_name = file.split('/')[-1]
    new_file = file[:-(len(list[-1])+1)]
    os.rename(file,new_file)
    pass
    #解析任务
    db.connect()
    try:
        task = Task.get(Task.finger == id)
    except:
        LOGR.debug('找不到对应任务：'+str(id))
        task = Task()
        task.finger = id
        task.name = ''
        task.dataType = '0'
        task.dir = ''
        task.username = ''
        task.password = ''
        task.target = ''
        task.port = ''
        task.tables = ''
        task.count = 0
        task.save()
        LOGR.info('发现新任务：' + str(id))
        exit(-1)
    #增加运行次数
    task.count = task.count + 1
    task.save()
    db.close()
    LOGR.info('开始任务：' + str(id)+":"+task.name)
    result = putData(task,new_file)
    #os.remove(new_file)
    if result:
        LOGR.info('任务执行完成：'+file)
    else:
        LOGR.info('任务执行失败：'+file)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        run(file)
    else:
        LOGR.error('参数错误,未提供任务id')
        exit(-1)
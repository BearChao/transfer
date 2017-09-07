#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:13
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_sender.py
# @Software: PyCharm
import multiprocessing
import os
import sys

import time

import redis

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
    os.remove(new_file)
    if result:
        LOGR.info('任务执行完成：'+file)
    else:
        LOGR.info('任务执行失败：'+file)

def worker():
    try:
        r = redis.Redis()
    except Exception as e:
        LOGR('redis连接失败，进程退出！')
        print(str(e))
        return -1
    while True:
        file = r.rpop('file')
        if file is not None:
            run(file.decode())
            time.sleep(1)


if __name__ == '__main__':

    p1 = multiprocessing.Process(target=worker)
    p1.daemon = True
    p1.start()
    LOGR.info('接收进程1启动成功')

    p2 = multiprocessing.Process(target=worker)
    p2.daemon = True
    p2.start()
    LOGR.info('接收进程2启动成功')

    p1.join()
    p2.join()

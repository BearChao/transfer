#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午7:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_receiver.py
# @Software: PyCharm
import os
import sys
import redis
from app.models import db, Task
from control.common import LOGS, LOGR
from control.common.file_and_folder import allow
from control.get_data.call_func import getDataFile

def run(id):
    if not allow():
        LOGS.error('系统激活失败，请联系厂家获取支持')
        return
    #解析任务
    db.connect()
    task = Task.get(Task.finger == id)
    if task is None:
        LOGS.error('找不到对应任务：'+str(id))
        exit(-1)
    # 增加运行次数
    task.count = task.count + 1
    task.save()
    db.close()
    LOGS.info('开始任务：' + str(id)+":"+task.name)

    #执行任务
    files =getDataFile(task)
    if len(files) == 0:
        LOGS.info('未获取到任何数据：' + str(id) + ':' + task.name)
        return 0

    #发送文件
    r = redis.Redis()
    for f in files:
        #subprocess.call('./transfer_file -s '+f, shell=True)
        #改为发送文件列表到redis
        print(f)
        r.lpush('file',f)
        #记录日志
    LOGS.info('数据加入发送队列，等待发送：'+str(id)+':'+task.name)

    # 删除文件
    # try:
    #     for f in files:
    #         os.remove(f)
    # except:
    #     pass

if __name__ == '__main__':

    if len(sys.argv) > 1:
        id = sys.argv[1]
        run(id)
    else:
        LOGS.error('参数错误,未提供文件名')
        exit(-1)

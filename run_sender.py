#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午7:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_receiver.py
# @Software: PyCharm
import os
import sys
import subprocess
from app.models import db, Task
from control.common import LOGS, LOGR
from control.get_data.call_func import getDataFile


def run(id):
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
    LOGR.info('开始任务：' + str(id)+":"+task.name)

    #执行任务
    files =getDataFile(task)

    #发送文件
    for f in files:
        subprocess.call('./transfer_file -s '+f, shell=True)

        #记录日志
    LOGR.info('数据传递完成')

    #删除文件
    try:
        for f in files:
            os.remove(f)
    except:
        pass

if __name__ == '__main__':

    if len(sys.argv) > 1:
        id = sys.argv[1]
        run(id)
    else:
        LOGS.error('参数错误,未提供文件名')
        exit(-1)
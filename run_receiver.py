#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午7:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : run_receiver.py
# @Software: PyCharm
import sys

from app.models import db, Task
from control.common import LOGS
from control.put_data.call_func import putData


def run(path):
    id_str = path.split('.')[-1]
    id = int(id_str)
    #解析任务
    db.connect()
    task = Task.get(Task.finger == id)
    if task is None:
        LOGS.error('找不到对应任务：'+str(id))
        exit(-1)
    db.close()
    LOGS.info('开始任务：' + str(id)+":"+task.name)

    #执行任务
    putData(task)

    LOGS.info('数据传递完成')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        path = sys.argv[1]
        run(path)
    else:
        LOGS.error('参数错误,未提供文件名')
        exit(-1)
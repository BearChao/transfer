#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 上午12:27
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : scheduler.py
# @Software: PyCharm
from crontab import CronTab

# 创建任务
def create_job(finger_str,minute,enable = True):
    cron = CronTab(user=True)
    command = 'cd /root/transfer && /usr/local/python3/bin/python3 run_sender.py ' + finger_str
    job = cron.new(command=command,comment=finger_str)
    job.minute.every(minute)

    job.enable(enable)
    cron.write()
    return True

def update_job_crontab(finger_str,minute,enable,index):
    cron = CronTab(user=True)
    iter = cron.find_comment(finger_str)
    list = []
    for i in iter:
        list.append(i)
    try:
        list[index].minute.every(minute)
        list[index].enable(enable)
        cron.write()
        return True
    except:
        return False

def delete_job_crontab(finger,index):
    cron = CronTab(user=True)
    iter = cron.find_comment(finger)
    list = []
    for i in iter:
        list.append(i)
    try:
        list[index].delete()
        cron.write()
        return True
    except:
        return False


def get_jobs(finger):
    cron = CronTab(user=True)
    iter = cron.find_comment(finger)
    list = []
    for i in iter:
        list.append(i)
    return list

def get_all_jobs():
    cron = CronTab(user=True)
    list = []
    for job in cron:
        list.append(job)
    return list

# # 设置任务执行周期，每两分钟执行一次
# job.setall('*/2 * * * *')
#
# job = cron.new(command='python -V')

# # 当然还支持其他更人性化的设置方式，简单列举一些
# job.minute.during(5, 50).every(5)
# job.hour.every(4)
# job.day.on(4, 5, 6)
#
#
# # 同时可以给任务设置comment，这样就可以根据comment查询，很方便
# job.set_comment("time log job")

# 根据comment查询，当时返回值是一个生成器对象，不能直接根据返回值判断任务是否#存在，如果只是判断任务是否存在，可直接遍历my_user_cron.crons


# 同时还支持根据command和执行周期查找，基本类似，不再列举

# 任务的disable和enable， 默认enable
# job.enable(False)
# job.enable()
#
# # 最后将crontab写入配置文件
# cron.write()



#
if __name__ == '__main__':
    jobs = get_all_jobs()
    for job in jobs:
        print(job.command)
        print(job.comment)
        print(job.last_run)
        print(job.is_enabled())
        print(job.is_valid())
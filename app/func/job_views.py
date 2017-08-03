#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 下午11:09
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : job_views.py
# @Software: PyCharm

from flask import render_template, request
from flask_login import login_required

from app.func.scheduler import get_jobs, update_job_crontab, delete_job_crontab
from control.common import LOGS
from . import func



@func.route('/job/edit/<finger>/<index>',methods=['POST','GET'])
@login_required
def edit_job_page(finger,index):
    jobs = get_jobs(finger)
    job = jobs[int(index)-1]
    return render_template('fragment/edit_job.html',job = job ,index = index)

@func.route('/job/update/', methods = ['POST'])
@login_required
def update_job():
    finger = request.form['finger']
    minute = int(request.form['minute'])
    index = int(request.form['index'])
    if not request.form['enable']:
        enable = False
    else:
        enable = True
    if update_job_crontab(finger, minute, enable, index):
        return render_template('auth/respond.json', state='success')
    else:
        return render_template('auth/respond.json', state='fail', message='操作失败')

@func.route('/job/delete/<finger>/<index>')
@login_required
def delete_job(finger,index):
    index = int(index) - 1
    if delete_job_crontab(finger,index):
        return render_template('auth/respond.json', state='success')
    else:
        return render_template('auth/respond.json', state='fail', message='操作失败')

@func.route('/job/run/<finger>')
@login_required
def run(finger):
    import subprocess
    try:
        out_bytes = subprocess.check_output('/usr/local/python3/bin/python3 run_sender.py '+ finger,shell=True,stderr=subprocess.PIPE)
    except Exception as e:
        LOGS.error('测试执行出现错误：'+str(e))
        return render_template('fragment/message.html',message = "运行过程中出现错误，请检查任务配置是否正常\n详情可参考日志")
    out = out_bytes.decode('utf-8')
    return render_template('fragment/message.html',message = out)


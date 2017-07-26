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

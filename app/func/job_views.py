#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 下午11:09
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : job_views.py
# @Software: PyCharm

from flask import render_template
from app.func.scheduler import  get_jobs
from . import func


@func.route('/job/edit/<finger>/<index>',methods=['POST','GET'])
def edit_job_page(finger,index):
    jobs = get_jobs(finger)
    job = jobs[int(index)-1]
    return render_template('fragment/edit_job.html',job = job)
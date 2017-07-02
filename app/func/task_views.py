from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app.func.forms import NewTaskForm
from app.func.scheduler import get_all_jobs, create_job, get_jobs
from app.main.views import common_list
from app.models import Task
from control.task.task import get_finger
from . import func


# 主页
@func.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('func/home.html')

#任务列表
@func.route('/task/list', methods=['GET'])
@login_required
def taskList():
    return common_list(Task,'func/tasklist.html')

#自动化管理
@func.route('/task/jobs')
def task_jobs():
    jobs = get_all_jobs()
    return common_list(Task,'func/taskJobs.html',arg=jobs)

#新建job页面
@func.route('/job/new/<finger>', methods=['POST','GET'])
def newJob(finger):
    return render_template('fragment/new_job.html', finger = finger)

#新建job操作
@func.route('/job/new',methods=['POST'])
def addJob():
    finger = request.form['finger']
    minute = int(request.form['minute'])
    enable = True
    if not request.form['enable']:
        enable = False
    if create_job(finger,minute,enable=enable):
        return render_template('auth/respond.json', state='success')
    else:
        return render_template('auth/respond.json', state='fail', message='操作失败')

#job详情
@func.route('/job/<finger>')
def jobDetail(finger):
    jobs = get_jobs(finger)
    return render_template('func/job_detail.html', jobs = jobs)


#删除任务
@func.route('/task/delete/<finger>')
def deleteTask(finger):
    try:
        task = Task.get(Task.finger == finger)
        task.delete_instance()
        return render_template('auth/respond.json',state='success')
    except:
        return render_template('auth/respond.json',state='fail',message='操作失败')


#新建任务
@func.route('/task/new', methods=['POST','GET'])
def newTask():
    form = NewTaskForm()
    if request.method == 'POST':

        if request.form['finger']:
            task = Task.get(finger = request.form['finger'])
        else:
            task = Task()
            task.finger = get_finger()
            task.count = 0
        task.dataType = request.form['dataType']
        task.name = request.form['name']
        task.dir = request.form['dir']
        task.username = request.form['username']
        task.password = request.form['password']
        task.port = request.form['port']
        task.tables = request.form['tables']
        task.target = request.form['target']
        #todo 检测参数是否正确
        task.save()
        return render_template('auth/respond.json',state="success")
    return render_template('fragment/new_task.html', form = form)

#编辑任务
@func.route('/task/edit/<finger>')
def editTask(finger):
    task = Task.get(Task.finger==finger)
    form = NewTaskForm()
    form.finger.data = task.finger
    form.dataType.data = task.dataType
    form.name.data = task.name
    form.dir.data = task.dir
    form.username.data = task.username
    form.password.data = task.password
    form.port.data = task.port
    form.tables.data = task.tables
    form.target.data = task.target
    form.count.data = task.count
    return render_template('fragment/new_task.html', form=form)

# #查看job详情
# @func.route('/job/<finger>')
# def get_jobs(finger):
#     jobs = get_jobs(finger)
#     return render_template('fragment/new_job.html', jobs = jobs)

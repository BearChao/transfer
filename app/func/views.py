from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app.func.forms import NewTaskForm
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


#弹出框组件
@func.route('/fragment/query')
def queryTask():
    return render_template('fragment/query.html')

@func.route('/fragment/new', methods=['POST','GET'])
def newTask():
    form = NewTaskForm()
    if request.method == 'POST':
        task = Task()
        task.finger = get_finger()
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
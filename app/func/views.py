from flask import render_template
from flask_login import login_required

from app.main.views import common_list
from app.models import Task
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

@func.route('/fragment/new')
def newTask():
    return render_template('fragment/new.html')
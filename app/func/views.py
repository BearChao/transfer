from flask import render_template
from flask_login import login_required

from . import func

# 主页
@func.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('func/home.html')

@func.route('/task/list', methods=['GET'])
@login_required
def taskList():
    return render_template('func/tasklist.html')



@func.route('/fragment/query')
def queryTask():
    return render_template('fragment/query.html')

@func.route('/fragment/new')
def newTask():
    return render_template('fragment/new.html')
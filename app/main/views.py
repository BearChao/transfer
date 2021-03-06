import hashlib
from os import listdir
import os
import subprocess
from os.path import isfile, join

from werkzeug.security import generate_password_hash

from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, send_from_directory
from flask_login import login_required, current_user
from app import utils
from app.main.forms import CfgNotifyForm, UserForm
from app.models import User
from . import main

logger = get_logger(__name__)
cfg = get_config()

# 通用列表查询
def common_list(DynamicModel, view, arg=None):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            # flash('删除成功')
            return render_template('auth/respond.json',state='success')
        except:
            # flash('删除失败')
            return render_template('auth/respond.json', state='fail', message = '操作失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}

    return render_template(view, form=dict, current_user=current_user,arg = arg)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            # if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.password = generate_password_hash(model.password)
                model.save()
                # flash('修改成功')
                return render_template('auth/respond.json',state='success')
            # else:
                 #utils.flash_errors(form)

    else:
        # 新增
        # if form.validate_on_submit():
        if request.method == 'POST':
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.password = generate_password_hash(model.password)
            model.save()
            return render_template('auth/respond.json',state='success')
            # flash('保存成功')
        # else:
        #     utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user,id= id)


# 首页跳转
@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user)

@main.route('/log/web/<page>')
@login_required
def log_web(page):
    page = int(page)
    count = 100
    with open('logs/web.log') as file:
        log = []
        i = j = 1
        for line in file:
            if i >= (page-1)*count:
                log.append(line)
                j+=1
            i+=1
            if j >= count:
                break
    return render_template('logs/web.html',log = log, page = page)


@main.route('/log/task')
@login_required
def log_task_list():
    mypath = 'logs/control'
    files = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('logs/crontrol_list.html',files = files)

@main.route('/log/download/<type>/<file>')
@login_required
def log_download(type,file):
    from flask import abort
    if type and file:
        file = file+'.log'
        path = current_app.root_path[:-3]
        if type == 'web':
            return send_from_directory(path+'logs','web.log',as_attachment=True)
        elif type == 'control':
            return send_from_directory(path+'logs/control',file,as_attachment=True)
        elif type == 'transfer':
            return send_from_directory(path+'logs/transfer',file,as_attachment=True)
        else:
            abort(404)
    else:

        abort(404)

@main.route('/log/task/<file>/<page>')
@login_required
def log_task(file,page):
    page = int(page)
    count = 100
    mypath = 'logs/control'
    with open(join(mypath,file+'.log')) as f:
        log = []
        i = j = 1
        for line in f:
            if i >= (page - 1) * count:
                log.append(line)
                j += 1
            i += 1
            if j >= count:
                break
    return render_template('logs/control.html', log=log, page=page, file = file,type='control')

@main.route('/log/file')
@login_required
def log_transfer_list():
    mypath = 'logs/transfer'
    files = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('logs/filetransfer_list.html',files = files)

@main.route('/log/file/<file>/<page>')
@login_required
def log_transfer(file,page):
    page = int(page)
    count = 100
    mypath = 'logs/transfer'
    with open(join(mypath,file+'.log')) as f:
        log = []
        i = j = 1
        for line in f:
            if i >= (page - 1) * count:
                log.append(line)
                j += 1
            i += 1
            if j >= count:
                break
    return render_template('logs/control.html', log=log, page=page, file = file,type='transfer')


@main.route('/log/delete')
@login_required
def log_delete():
    if request.args.get('type'):
        state = 'success'
        message = ''
        type = request.args.get('type')
        if type == '1':  #web日志
            if not utils.del_web_log():
                state = 'fail'
                message = '操作失败！'
        elif type == '2': #任务日志
            num = request.args.get('num')
            if not utils.del_control_log(int(num)):
                state = 'fail'
                message = '操作失败！'
        elif type == '3': #文件传输日志
            num = request.args.get('num')
            if not utils.del_transfer_log(int(num)):
                state = 'fail'
                message = '操作失败,可能日志已经清空'
        return render_template('auth/respond.json',state = state, message = message)
    else:
        return render_template('logs/clear.html')

@main.route('/json/nav')
def nav():
    if current_user.role == 2:
        return render_template('nav.log.json')
    if current_app.config.get('CLIENT_TYPE') == 'receiver':
        return render_template('nav.recv.json')
    return render_template('nav.json')

@main.route('/user')
@login_required
def user_list():
    return common_list(User,'user/user_list.html')

@main.route('/user/edit',methods=['POST','GET'])
@login_required
def edit_user():
    userForm = UserForm()
    return common_edit(User,userForm,'user/user_edit.html')

@main.route('/user/new')
@login_required
def new_user():
    userForm = UserForm()
    return common_edit(User,userForm,'user/user_new.html')

@main.route('/clear')
@login_required
def clear():
    try:
        __import__('shutil').rmtree('temp')
        os.mkdir('temp')
    except:
        return render_template('auth/respond.json',state = 'fail',message = "操作失败，请稍后再试...")
    return render_template('auth/respond.json',state = 'success')

@main.route('/uploadkey', methods=['POST'])
def uploadkey():
    file = request.files['file']
    path = 'temp/key.temp.key'
    file.save(path)
    m = hashlib.md5()
    m.update(open(path,'rb').read())
    out = m.hexdigest()
    os.remove(path)
    if out == '2d6e56adabb2d726d15b5e59eda061d4':
        open("conf/auth", "w+").close()
        return render_template('auth/message.html',message= '激活成功！请重新登录')
    return render_template('auth/message.html',message= '激活失败！请检查激活文件是否正确')

import monitor
@main.route('/info',methods=['POST','get'])
@login_required
def get_info():
    dict = {}
    dict['cpu'] = monitor.cpuinfo()
    dict['mem'],dict['mem_free'] = monitor.meminfo()
    return jsonify(dict)

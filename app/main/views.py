from os import listdir

from os.path import isfile, join

from werkzeug.security import generate_password_hash

from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request, current_app
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
    return render_template('logs/control.html', log=log, page=page, file = file)

@main.route('/log/file')
@login_required
def log_transfer_list():
    mypath = 'logs/transfer'
    files = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('logs/crontrol_list.html',files = files)

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
    return render_template('logs/control.html', log=log, page=page, file = file)


@main.route('/log/delete')
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
                message = '操作失败'
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
def user_list():
    return common_list(User,'user/user_list.html')

@main.route('/user/edit',methods=['POST','GET'])
def edit_user():
    userForm = UserForm()
    return common_edit(User,userForm,'user/user_edit.html')

@main.route('/user/new')
def new_user():
    userForm = UserForm()
    return common_edit(User,userForm,'user/user_new.html')
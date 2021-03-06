
from flask import render_template, redirect, request, url_for, flash, jsonify, current_app

from control.common import LOGS
from . import auth
from .forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #print(form.rememberme.data)
    if form.validate_on_submit():
        try:
            user = User.get(User.username == form.username.data)
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('用户名或密码错误')
        except Exception as e:
            LOGS.error(repr(e))
            flash('用户名不存在')
    stat = '外网端'
    if current_app.config.get('CLIENT_TYPE') == 'receiver':
        stat = '内网端'
    return render_template('auth/login.html', form=form, stat = stat)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    referer = 'http://'+ request.host + url_for('auth.login')
    #flash('您已退出登录')
    state = "success"
    message = "提交成功"
    return render_template('auth/respond.json', state = state, message = message, referer = referer)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 下午10:53
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : ipconfig_view.py
# @Software: PyCharm
from flask import request, render_template
from flask_login import login_required

from . import func


@func.route('/netcard',methods=['POST','GET'])
@login_required
def ipconfig():
    '''
    设置ip地址：
    device:设备
    ip:IPd地址
    mask:子网掩码
    gateway:网关地址
    :return:
    '''
    if request.form.get('device'):
        device = request.form.get('device')
        ip = request.form.get('ip')
        mask = request.form.get('mask')
        gateway = request.form.get('gateway')
        if device == 'eth1':
            pass
        elif device == 'eth2':
            pass
        elif device == 'eth3':
            pass
        elif device == 'eth4':
            pass
        elif device == 'eth5':
            pass
        #todo 设置ip地址
        return render_template('auth/respond.json',state = 'success')
    else:
        #todo 查询所有ip文件
        return render_template('func/netcard.html')
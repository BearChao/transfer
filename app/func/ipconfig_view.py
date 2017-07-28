#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 下午10:53
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : ipconfig_view.py
# @Software: PyCharm
from flask import request, render_template
from flask_login import login_required
import subprocess
from control.common import LOGS
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
        result = True
        if device == 'eth0':
            result = changeNetwork('eth3',ip,mask,gateway)
        elif device == 'eth1':
            result = changeNetwork('eth4', ip, mask, gateway)
        elif device == 'eth2':
            result = changeNetwork('eth5', ip, mask, gateway)
        elif device == 'eth3':
            result = changeNetwork('eth6', ip, mask, gateway)
        if result:
            message = '操作成功！'
        else:
            message = '操作失败！'
        return render_template('auth/respond.json',state = 'success', message = message)
    else:
        return render_template('func/netcard.html')

def changeNetwork(device,ip,netmask,gateway):
    """
    @attention: change the network of the system
    """
    path = "/etc/sysconfig/network-scripts/ifcfg-" + str(device)
    file_handler = open(path, "r")
    network_content = file_handler.read()
    file_handler.close()
    conte = "IPADDR=%s\nNETMASK=%s\nGATEWAY=%s\n" % (ip, netmask, gateway)
    num = network_content.find("IPADDR")
    if num != -1:
        network_content = network_content[:num] + conte
        file_handler = open(path, "w")
        file_handler.write(network_content)
        file_handler.close()
    result = subprocess.call("sudo ifdown %s && sudo ifup %s" % (device, device),shell=True)
    if result == 0:
        LOGS.info('ip修改成功：%s:%s:%s:%s',device,ip,gateway,netmask)
        return True
    else:
        LOGS.info('ip修改失败：%s:%s:%s:%s', device, ip, gateway, netmask)
        return False

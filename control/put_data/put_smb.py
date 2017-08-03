#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/29 下午3:07
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : put_smb.py
# @Software: PyCharm
import os

from smb.SMBConnection import SMBConnection

from control.common import LOGR


def putSMB(task,file):
    try:
        samba = SMBConnection(task.username, task.password, 'mybase', task.target)
        samba.connect(task.dir, int(task.port))
        list = task.tables.split(' ')
        share = list[0] #TESt
        path = list[1]  #/
        s = file.split('/')[1]
        l = len(s)+1+5
        t = file[l:]  #temp/share/  ddddd
        if path[-1]=='/':
            path += t   #/ddd
        else:
            path = path+'/'+t
        # 取路径
        dir = os.path.split(path)[0]
        # 去除首位空格
        dir = dir.strip()
        # 去除尾部 \ 符号
        dir = dir.rstrip("\\")
        if dir != '/':
            mkdir(samba,share,dir)
        with open(file,'rb') as f:
            samba.storeFile(share,path,f)
        return True
    except Exception as e:
        LOGR.error('发送SMB文件错误：'+str(e))

def mkdir(samba,share,dir):  #/forder/test
    temp = ''
    path_list = dir.split('/')
    for d in path_list:
        if d == '':
            continue
        temp += '/'+ d
        try:
            samba.createDirectory(share,temp)
        except:
            continue






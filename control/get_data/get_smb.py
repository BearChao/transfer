#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 上午10:48
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : get_smb.py
# @Software: PyCharm

from smb.SMBConnection import *
from control.common import LOGS

# # 初始化一个samba访问对象
# samba = SMBConnection('zynick', 'define', 'Name', 'ZYNICK-PC')
# # 创建一个samba连接
# samba.connect('192.168.31.126')  # 返回True/False
# # 从服务器获取文件列表
# flist = samba.listPath('GoPro', '/forder')  # 返回的是文件对象组成的元组，注意返回结果里面包含所有文件甚至是 . 和 .. 也会包含进去。
# for f in flist:
#     print(f.filename)
# # 下载文件到本地
# f = open('本地文件', 'w')  # 就是要下载下来存放的那个文件的壳子
# samba.retrieveFile('共享空间', '服务器文件地址', f)  # 它会把文件写在f里面
# f.close()
# # 上传文件到服务器
# f = open('本地文件', 'r')
# samba.storeFile('共享空间', '服务器文件地址', f)
# f.close()
from control.common.file_and_folder import mkdir


def getSMB(task):
    files = []
    try:
        samba = SMBConnection(task.username,task.password,'mybase',task.target)
        samba.connect(task.dir,int(task.port))
        list = task.tables.split(' ')
        share = list[0]
        path = list[1]
        id_str = str(task.finger)
        if len(list) == 3: #指定文件
            file = list[2]
            p = path + '/' + file
            retrieveFile(samba,share,p,id_str)
            files.append(p)
        else:
            list = retrieveFileList(samba,share,path)
            for l in list:
                retrieveFile(samba,share,l,id_str)
                files.append(l)
        return files

    except Exception as e:
        LOGS.error('SMB连接出错:'+str(e))

def retrieveFileList(samba,share,path):
    result = []
    files = samba.listPath(share, path)
    files = files[2:]  # 去除. ..
    for f in files:
        if f.isDirectory:
            if path[-1]=='/':
                dir = path+f.filename
            else:
                dir = path+'/'+f.filename
            result+= retrieveFileList(samba,share,dir)
        else:
            if path[-1]=='/':
                file = path+f.filename
            else:
                file = path+'/'+f.filename
            result.append(file)
    return result

def retrieveFile(samba,share,path,id_str):
    file_path = 'temp/' + share + path + '.' + id_str
    try:
        mkdir(file_path)
        with open(file_path, 'wb') as f:
            samba.retrieveFile(share, path, f)
            LOGS.info('获取文件：' + path)
    except Exception as e:
        LOGS.error('SMB获取文件错误：'+str(e))
    return file_path
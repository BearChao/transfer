#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 上午10:48
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : get_smb.py
# @Software: PyCharm

from smb.SMBConnection import *
from smb.base import SharedFile
from smb.SMBProtocol import *

# 初始化一个samba访问对象
samba = SMBConnection('zynick', 'define', 'Name', '//zynick-pc')
# 创建一个samba连接
samba.connect('192.168.31.226')  # 返回True/False
# 从服务器获取文件列表
flist = samba.listPath('\GoPro', '')  # 返回的是文件对象组成的元组，注意返回结果里面包含所有文件甚至是 . 和 .. 也会包含进去。
print(flist)
# # 下载文件到本地
# f = open('本地文件', 'w')  # 就是要下载下来存放的那个文件的壳子
# samba.retrieveFile('共享空间', '服务器文件地址', f)  # 它会把文件写在f里面
# f.close()
# # 上传文件到服务器
# f = open('本地文件', 'r')
# samba.storeFile('共享空间', '服务器文件地址', f)
# f.close()
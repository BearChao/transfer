#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/29 下午2:33
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : testSMB.py
# @Software: PyCharm

# 初始化一个samba访问对象
from smb.SMBConnection import SMBConnection

samba = SMBConnection('zynick', 'define', 'Name', 'ZYNICK-PC')
# 创建一个samba连接
samba.connect('192.168.31.126')  # 返回True/False
# 从服务器获取文件列表
flist = samba.listPath('GoPro', '/forder')  # 返回的是文件对象组成的元组，注意返回结果里面包含所有文件甚至是 . 和 .. 也会包含进去。
for f in flist:
    print(f.filename)
# 下载文件到本地
with open('本地文件', 'wb') as f: # 就是要下载下来存放的那个文件的壳子
    samba.retrieveFile('GoPro', '/forder/text.txt', f)  # 它会把文件写在f里面

# 上传文件到服务器
# f = open('本地文件', 'rb')
# samba.storeFile('共享空间', '服务器文件地址', f)
# f.close()
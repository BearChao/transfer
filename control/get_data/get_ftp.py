#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午8:04
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : get_ftp.py
# @Software: PyCharm
import ftplib
from ftplib import FTP
import os, sys, string, datetime, time


def getFTP(task):
    conn = MyFTP(task.target, int(task.port), str(task.finger))
    conn.Login(task.username, task.password)
    list = conn.DownLoadFileTree('temp', task.dir)
    conn.quit()
    return list


class MyFTP:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""
    finger = ""
    list = []

    def __init__(self, host, port=21, finger='temp'):
        self.ftp.connect(host, port=port)
        self.finger = finger

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        self.ftp.set_pasv(True)
        self.ftp.encoding = 'utf8'
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):
        file = LocalFile + '.' + self.finger
        file_handler = open(file, 'wb')
        self.ftp.retrbinary('RETR %s' % (RemoteFile), file_handler.write)
        file_handler.close()
        return file

    def UpLoadFile(self, LocalFile, RemoteFile):
        # 文件不存在
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")

        dirname = os.path.dirname(RemoteFile)
        file_name = os.path.basename(RemoteFile)
        if self.isDir(dirname):
            self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)
        else:
            dest_dirname = dirname.split('/')
            for subdir in dest_dirname:
                try:
                    self.ftp.cwd(subdir)
                except ftplib.error_perm:
                    self.ftp.mkd(subdir)
                    self.ftp.cwd(subdir)
            self.ftp.storbinary('STOR %s' % file_name, file_handler, 4096)

        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False

        LocalNames = os.listdir(LocalDir)

        self.ftp.cwd(RemoteDir)

        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):

        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)

        RemoteNames = self.ftp.nlst()

        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                l = self.DownLoadFile(Local, file)
                self.list.append(l)
        self.ftp.cwd("..")
        return self.list

    def show(self, list):
        result = list.lower().split(" ")

        if self.path.split(" ")[-1] in result and result[0].startswith('d'):
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)

        return self.bIsDir

    def quit(self):
        self.ftp.quit()


if __name__ == '__main__':
    # ftp = FTPSync('127.0.0.1', 21, '测试')
    # ftp.login('zynick', 'define')
    ftp = MyFTP('192.168.1.200')
    ftp.Login('xaleap', 'admin123')

    # 上传文件，不重命名
    # ftp.put_file('111.txt','a/b')
    # 上传文件，重命名
    # ftp.put_file('111.txt','a/112.txt')
    # 下载文件，不重命名
    # ftp.get_file('/a/111.txt',r'D:\\')
    # 下载文件，重命名
    # ftp.get_file('/a/111.txt',r'D:\112.txt')
    # 下载到已经存在的文件夹
    # ftp.get_dir('a/b/c',r'D:\\a')
    # 下载到不存在的文件夹
    # ftp.get_dir('a/b/c',r'D:\\aa')
    # 上传到已经存在的文件夹
    # ftp.put_dir('b','a')
    # 上传到不存在的文件夹
    # ftp.put_dir('b','aa/B/')

    # a = ftp.DownLoadFileTree('/Users/zynick/temp', 'a')
    # print(a)

    #ftp.UpLoadFile('/Users/zynick/Pictures/wall/img_0284.jpg','a/b/c/d.txt')
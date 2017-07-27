#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 下午9:28
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : put_mysql.py
# @Software: PyCharm
import os
import pickle

import mysql.connector

from control.common import LOGR
from control.get_data.get_mysql import MySQLClient

def putMySQL(configItem,file):

    try:
        conn = mysql.connector.connect(host=configItem.dir,username=configItem.username,password=configItem.password,database=configItem.target)
        with open(file,'rb') as f:
            data = pickle.load(f)
        #拼凑导入sql
        table = os.path.basename(file).split('.')[0]
        sql = 'INSERT INTO ' + table +' VALUES('
        length = len(data[0])
        for i in range(length):
            sql += '%s'
            if i < length - 1:
                sql += ','
        sql += ')'
        #导入
        cur = conn.cursor()
        cur.executemany(sql,data)
    except:
        LOGR.info('写入数据库出错，常见错误为数据库id重复')
        return False
    return True

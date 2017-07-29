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
        conn = mysql.connector.connect(host=configItem.dir,user=configItem.username,password=configItem.password,database=configItem.target)
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
        conn.commit()
        conn.close()
    except Exception as e:
        LOGR.error('写入数据库出错:'+ str(e))
        return False
    return True

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/19 下午8:47
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : get_mysql.py
# @Software: PyCharm
import pickle
import mysql.connector

from app.models import Task
from control.common import LOGS


def getMySQL(configItem):

    db = MySQLClient(host=configItem.dir,username=configItem.username,password=configItem.password,database=configItem.target)
    if configItem.tables is None or configItem.tables == '' or configItem.tables == ' ':
        return db.getAllData(str(configItem.finger))
    else:
        files = []
        tables = configItem.tables.split(" ")
        for t in tables:
            files.append(db.getData(t,str(configItem.finger)))
        return files

class MySQLClient:

    def __init__(self,host,username,password,database=None):
        try:
            if database == '' or database is None:
                self.conn = mysql.connector.connect(host=host,user=username, password=password)
            self.conn = mysql.connector.connect(host=host,user=username, password=password, database=database)
        except Exception as e:
            LOGS.error(str(e))

    def getDatabases(self):
        '''
        获得数据库列表
        :param type:
        :return:数据库列表list
        '''
        cur = self.conn.cursor()
        cur.execute('show databases;')
        result = cur.fetchall()
        databases = []
        for r in result:
            databases.append(r[0])
        cur.close()
        return databases

    def getTables(self):
        cur = self.conn.cursor()
        cur.execute('show tables;')
        tables = []
        for t in cur.fetchall():
            tables.append(t[0])
        cur.close()
        return tables

    def useDatabase(self,database):
        cur = self.conn.cursor()
        cur.execute('use %s;' %database)
        cur.close()

    def getData(self,table,id_str):
        LOGS.debug('获取表数据：'+table)
        try:
            cur = self.conn.cursor()
            cur.execute('select * from %s;' %table)
            data = cur.fetchall() #list: [(1, '1', None), (2, '2', '2')]
            cur.close()
            LOGS.info('获取表数据完成：' + table)
            file = 'temp/'+table+'.'+id_str  #命名规则：表名.任务id
            f = open(file, 'wb')
            pickle.dump(data, f)
            f.close()
            LOGS.debug('保存数据完成：'+file)
            return file
        except Exception as e:
            LOGS.error(str(e))
            return '-'


    def getAllData(self,id_str):
        tables = self.getTables()
        files = []
        for t in tables:
            files.append(self.getData(t,id_str))
        return files

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = MySQLClient(host='139.199.212.48',username='root',password='123456',database='test')
    item = Task()
    item.dir = '139.199.212.48'
    item.username = 'root'
    item.password = '123456'
    item.target = 'test'
    item.id = 20170620003312

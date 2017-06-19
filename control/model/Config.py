#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午10:22
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : Config.py
# @Software: PyCharm
from enum import Enum
import time
import common.dict_json


class DATATYPE(Enum):
    FILE = 1
    FTP = 2
    WEBDAV = 3
    #>10则为数据库类型
    MYSQL = 11
    ORACLE = 12
    #todo 枚举中添加其他类型


class ConfigItem():
    """
    id:任务id
    name:任务名称
    dataType:数据来源
    dir:数据目录或者连接字符串
    username:登录用户
    password：登录密码

    """
    def __init__(self, name='', dataType=DATATYPE.FILE, dir='', username='', password='', id=None, target='',port=0):
        if id is None:
            self.id = int(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        else:
            self.id = int(id)
        self.name = name
        self.dataType = dataType
        self.dir = dir
        self.username = username
        self.password = password
        self.target = target
        self.port = port


    def isDatabase(self):
        if self.dataType >10:
            return True
        else:
            return False

    def to_dict(self):
        d = dict(
            id = self.id,
            name = self.name,
            dataType = self.dataType.value,
            dir = self.dir,
            username = self.username,
            password = self.password,
            target = self.target,
            port = self.port
        )
        return d

class Config():
    #配置文件类
    def __init__(self):
        self.configs = []

    def addConfigItem(self,configItem):
        #添加配置项
        self.configs.append(configItem)

    def delConfigItem(self,id):
        #删除配置项
        for i in self.configs:
            if i.id == id:
                self.configs.remove(i)
                return True
            else:
                return False

    def getConfigItem(self,id):
        for i in self.configs:
            if i.id == id:
                return i
            else:
                return None

    def getNum(self):
        return len(self.configs)

    def save(self):
        l = []
        for i in self.configs:
            l.append(i.to_dict())
        common.dict_json.saveConfig(l)

    def load(self):
        self.__init__()
        result = common.dict_json.loadConfig()
        for i in result:
            item = ConfigItem(id=i['id'], name=i['name'], dataType=i['dataType'], dir=i['dir'], username=i['username'], password=i['password'],
                              target= i['target'], port = i['port'])
            self.configs.append(item)

if __name__ == '__main__':
    conf = ConfigItem()
    c = Config()
    # c.addConfigItem(conf)
    # c.addConfigItem(conf)
    # c.addConfigItem(conf)
    # c.save()
    c.load()
    print(c.getNum())
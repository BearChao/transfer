#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午5:39
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : dict_json.py
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:25
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : dict_json.py
# @Software: PyCharm
import json

#config要求为一个列表，列表中为config项
from common import CONFIGFILE


def saveConfig(data):

    with open(CONFIGFILE,'w') as f:
        json.dump(data,f)

def loadConfig():

    with open(CONFIGFILE,'r') as f:
        j = json.load(f)
        return j



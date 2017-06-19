#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/12 下午9:16
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : __init__.py.py
# @Software: PyCharm
from common import logger

CONFIGFILE = "conf/config.json"
LOGS = logger.Logger("Sender")
LOGR = logger.Logger("Receiver")
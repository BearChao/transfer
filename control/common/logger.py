#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 下午6:47
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : logger.py
# @Software: PyCharm

# create logger
import logging
import time

import sys


class Logger:
    """
    logger的配置
    """

    def __init__(self, name):
        logger_name = name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler
        file = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log_path = "logs/control/" + file + ".log"
        fh = logging.FileHandler(log_path)
        sh = logging.StreamHandler(stream=sys.stdout)

        # create formatter
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        fmt2 = '%(message)s'
        formatter2 = logging.Formatter(fmt2)

        # add handler and formatter to logger
        fh.setFormatter(formatter)
        sh.setFormatter(formatter2)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)


    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)

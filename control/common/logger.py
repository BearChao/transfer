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
        log_path = "log/" + file + ".log"
        fh = logging.FileHandler(log_path)

        # create formatter
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        # add handler and formatter to logger
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)


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

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import logging
import inspect
import datetime
from logging.handlers import RotatingFileHandler


current_path = os.getcwd()
log_dir = os.path.join(current_path, 'gateway-Log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

handlers = {logging.ERROR: os.path.join(current_path, 'gateway-Log/error.log'),
            logging.DEBUG: os.path.join(current_path, 'gateway-Log/debug.log'),
            logging.INFO: os.path.join(current_path, 'gateway-Log/info.log')}

def createHandlers():
    logLevels = handlers.keys()
    for level in logLevels:
        path = os.path.abspath(handlers[level])
        # 设置写入文件，文件大小超过10M时，切割日志文件，仅保留3个文件
        handlers[level] = RotatingFileHandler(filename=path, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')

# 加载模块时创建全局变量
createHandlers()


class OutPutLog(object):
    '''
    该日志类可以把不同级别的日志按照日期输出到不同的日志文件中
    '''

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        logLevels = handlers.keys()
        for level in logLevels:
            logger = logging.getLogger(str(level))
            # 如果不指定level，获得的handler似乎是同一个handler?
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] 文件路径-日志级别 [行号]: 具体信息'''
        res = "[%s] %s-%s [%s]：%s" % (self.printfNow(), filename, level, lineNo, message)
        return res


    def info(self, message):
        message = self.getLogMessage("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)
        self.__loggers[logging.ERROR].error(message)

    def debug(self, message):
        message = self.getLogMessage("debug", message)
        self.__loggers[logging.DEBUG].debug(message)
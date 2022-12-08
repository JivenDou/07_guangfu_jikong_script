"""
@File  : log_config.py
@Author: lee
@Date  : 2022/7/13/0013 11:08:55
@Desc  :
"""
import logging
import sys

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        # 新曾自定义日志，用于数据采集程序
        "general": {
            "level": "INFO",
            "handlers": ["console", "general"],
            "propagate": True,
            "qualname": "general.debug",
        },
        "tcp_connector": {
            "level": "DEBUG",
            "handlers": ["console", "tcp_connector"],
            "propagate": True,
            "qualname": "tcp_connector.debug",
        },
        "zuhe_tcp_connector": {
            "level": "DEBUG",
            "handlers": ["console", "zuhe_tcp_connector"],
            "propagate": True,
            "qualname": "zuhe_tcp_connector.debug",
        },
        "modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "modbus_connector"],
            "propagate": True,
            "qualname": "modbus_connector.debug",
        },
        "zuhe_converter": {
            "level": "DEBUG",
            "handlers": ["console", "zuhe_converter"],
            "propagate": True,
            "qualname": "zuhe_converter.debug",
        },
        "modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "modbus_converter"],
            "propagate": True,
            "qualname": "modbus_converter.debug",
        },
    },
    handlers={
        # 数据采集程序控制台输出handler
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "general": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/general/general.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "tcp_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/tcp_connector/tcp_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "zuhe_tcp_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/zuhe_tcp_connector/zuhe_tcp_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/modbus_connector/modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "zuhe_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/zuhe_converter/zuhe_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/modbus_converter_log/modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        }
    },
    formatters={
        # 自定义文件格式化器
        "generic": {
            "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
            "class": "logging.Formatter",
        }
    },
)
general = logging.getLogger("general")
tcp_connector = logging.getLogger("tcp_connector")
zuhe_tcp_connector = logging.getLogger("zuhe_tcp_connector")
modbus_connector = logging.getLogger("modbus_connector")
zuhe_converter = logging.getLogger("zuhe_converter")
modbus_converter = logging.getLogger("modbus_converter")

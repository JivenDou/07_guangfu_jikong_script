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
        "zuhe_tcp_connector": {
            "level": "DEBUG",
            "handlers": ["console", "zuhe_tcp_connector"],
            "propagate": True,
            "qualname": "zuhe_tcp_connector.debug",
        },
        "yingli1_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "yingli1_modbus_connector"],
            "propagate": True,
            "qualname": "yingli1_modbus_connector.debug",
        },
        "yingli2_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "yingli2_modbus_connector"],
            "propagate": True,
            "qualname": "yingli2_modbus_connector.debug",
        },
        "leida_fuzhao_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "leida_fuzhao_modbus_connector"],
            "propagate": True,
            "qualname": "leida_fuzhao_modbus_connector.debug",
        },
        "atesi_fuzhao_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "atesi_fuzhao_modbus_connector"],
            "propagate": True,
            "qualname": "atesi_fuzhao_modbus_connector.debug",
        },
        "jingke1_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "jingke1_modbus_connector"],
            "propagate": True,
            "qualname": "jingke1_modbus_connector.debug",
        },
        "jingke2_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "jingke2_modbus_connector"],
            "propagate": True,
            "qualname": "jingke2_modbus_connector.debug",
        },
        "a_pingtai_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "a_pingtai_modbus_connector"],
            "propagate": True,
            "qualname": "a_pingtai_modbus_connector.debug",
        },
        "b_pingtai_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "b_pingtai_modbus_connector"],
            "propagate": True,
            "qualname": "b_pingtai_modbus_connector.debug",
        },
        "c_pingtai_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "c_pingtai_modbus_connector"],
            "propagate": True,
            "qualname": "c_pingtai_modbus_connector.debug",
        },
        "d_pingtai_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "d_pingtai_modbus_connector"],
            "propagate": True,
            "qualname": "d_pingtai_modbus_connector.debug",
        },
        "moxa5430_1_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_1_modbus_connector"],
            "propagate": True,
            "qualname": "moxa5430_1_modbus_connector.debug",
        },
        "moxa5430_3_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_3_modbus_connector"],
            "propagate": True,
            "qualname": "moxa5430_3_modbus_connector.debug",
        },
        "moxa5430_4_modbus_connector": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_4_modbus_connector"],
            "propagate": True,
            "qualname": "moxa5430_4_modbus_connector.debug",
        },
        "zuhe_converter": {
            "level": "DEBUG",
            "handlers": ["console", "zuhe_converter"],
            "propagate": True,
            "qualname": "zuhe_converter.debug",
        },
        "yingli1_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "yingli1_modbus_converter"],
            "propagate": True,
            "qualname": "yingli1_modbus_converter.debug",
        },
        "yingli2_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "yingli2_modbus_converter"],
            "propagate": True,
            "qualname": "yingli2_modbus_converter.debug",
        },
        "leida_fuzhao_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "leida_fuzhao_modbus_converter"],
            "propagate": True,
            "qualname": "leida_fuzhao_modbus_converter.debug",
        },
        "atesi_fuzhao_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "atesi_fuzhao_modbus_converter"],
            "propagate": True,
            "qualname": "atesi_fuzhao_modbus_converter.debug",
        },
        "jingke1_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "jingke1_modbus_converter"],
            "propagate": True,
            "qualname": "jingke1_modbus_converter.debug",
        },
        "jingke2_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "jingke2_modbus_converter"],
            "propagate": True,
            "qualname": "jingke2_modbus_converter.debug",
        },
        "a_pingtai_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "a_pingtai_modbus_converter"],
            "propagate": True,
            "qualname": "a_pingtai_modbus_converter.debug",
        },
        "b_pingtai_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "b_pingtai_modbus_converter"],
            "propagate": True,
            "qualname": "b_pingtai_modbus_converter.debug",
        },
        "c_pingtai_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "c_pingtai_modbus_converter"],
            "propagate": True,
            "qualname": "c_pingtai_modbus_converter.debug",
        },
        "d_pingtai_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "d_pingtai_modbus_converter"],
            "propagate": True,
            "qualname": "d_pingtai_modbus_converter.debug",
        },
        "moxa5430_1_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_1_modbus_converter"],
            "propagate": True,
            "qualname": "moxa5430_1_modbus_converter.debug",
        },
        "moxa5430_3_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_3_modbus_converter"],
            "propagate": True,
            "qualname": "moxa5430_3_modbus_converter.debug",
        },
        "moxa5430_4_modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "moxa5430_4_modbus_converter"],
            "propagate": True,
            "qualname": "moxa5430_4_modbus_converter.debug",
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
        "zuhe_tcp_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/zuhe_tcp_connector/zuhe_tcp_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "yingli1_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/yingli1_modbus_connector/yingli1_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "yingli2_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/yingli2_modbus_connector/yingli2_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "leida_fuzhao_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/leida_fuzhao_modbus_connector/leida_fuzhao_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "atesi_fuzhao_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/atesi_fuzhao_modbus_connector/atesi_fuzhao_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "jingke1_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/jingke1_modbus_connector/jingke1_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "jingke2_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/jingke2_modbus_connector/jingke2_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "a_pingtai_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/a_pingtai_modbus_connector/a_pingtai_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "b_pingtai_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/b_pingtai_modbus_connector/b_pingtai_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "c_pingtai_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/c_pingtai_modbus_connector/c_pingtai_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "d_pingtai_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/d_pingtai_modbus_connector/d_pingtai_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_1_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_1_modbus_connector/moxa5430_1_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_3_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_3_modbus_connector/moxa5430_3_modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_4_modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_4_modbus_connector/moxa5430_4_modbus_connector.log',
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
        "yingli1_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/yingli1_modbus_converter/yingli1_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "yingli2_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/yingli2_modbus_converter/yingli2_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "leida_fuzhao_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/leida_fuzhao_modbus_converter/leida_fuzhao_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "atesi_fuzhao_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/atesi_fuzhao_modbus_converter/atesi_fuzhao_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "jingke1_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/jingke1_modbus_converter/jingke1_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "jingke2_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/jingke2_modbus_converter/jingke2_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "a_pingtai_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/a_pingtai_modbus_converter/a_pingtai_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "b_pingtai_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/b_pingtai_modbus_converter/b_pingtai_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "c_pingtai_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/c_pingtai_modbus_converter/c_pingtai_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "d_pingtai_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/d_pingtai_modbus_converter/d_pingtai_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_1_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_1_modbus_converter/moxa5430_1_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_3_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_3_modbus_converter/moxa5430_3_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "moxa5430_4_modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/moxa5430_4_modbus_converter/moxa5430_4_modbus_converter_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
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
# 连接器
zuhe_tcp_connector = logging.getLogger("zuhe_tcp_connector")
yingli1_modbus_connector = logging.getLogger("yingli1_modbus_connector")
yingli2_modbus_connector = logging.getLogger("yingli2_modbus_connector")
leida_fuzhao_modbus_connector = logging.getLogger("leida_fuzhao_modbus_connector")
atesi_fuzhao_modbus_connector = logging.getLogger("atesi_fuzhao_modbus_connector")
jingke1_modbus_connector = logging.getLogger("jingke1_modbus_connector")
jingke2_modbus_connector = logging.getLogger("jingke2_modbus_connector")
a_pingtai_modbus_connector = logging.getLogger("a_pingtai_modbus_connector")
b_pingtai_modbus_connector = logging.getLogger("b_pingtai_modbus_connector")
c_pingtai_modbus_connector = logging.getLogger("c_pingtai_modbus_connector")
d_pingtai_modbus_connector = logging.getLogger("d_pingtai_modbus_connector")
moxa5430_1_modbus_connector = logging.getLogger("moxa5430_1_modbus_connector")
moxa5430_3_modbus_connector = logging.getLogger("moxa5430_3_modbus_connector")
moxa5430_4_modbus_connector = logging.getLogger("moxa5430_4_modbus_connector")
# 解析器
zuhe_converter = logging.getLogger("zuhe_converter")
yingli1_modbus_converter = logging.getLogger("yingli1_modbus_converter")
yingli2_modbus_converter = logging.getLogger("yingli2_modbus_converter")
leida_fuzhao_modbus_converter = logging.getLogger("leida_fuzhao_modbus_converter")
atesi_fuzhao_modbus_converter = logging.getLogger("atesi_fuzhao_modbus_converter")
jingke1_modbus_converter = logging.getLogger("jingke1_modbus_converter")
jingke2_modbus_converter = logging.getLogger("jingke2_modbus_converter")
a_pingtai_modbus_converter = logging.getLogger("a_pingtai_modbus_converter")
b_pingtai_modbus_converter = logging.getLogger("b_pingtai_modbus_converter")
c_pingtai_modbus_converter = logging.getLogger("c_pingtai_modbus_converter")
d_pingtai_modbus_converter = logging.getLogger("d_pingtai_modbus_converter")
moxa5430_1_modbus_converter = logging.getLogger("moxa5430_1_modbus_converter")
moxa5430_3_modbus_converter = logging.getLogger("moxa5430_3_modbus_converter")
moxa5430_4_modbus_converter = logging.getLogger("moxa5430_4_modbus_converter")

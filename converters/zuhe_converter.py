"""
@File  : cec21_converter.py
@Author: lee
@Date  : 2022/8/30/0030 14:42:02
@Desc  : 姿态定位组合传感器
"""
from logging_config import zuhe_converter as logger
from converter import Converter
from tools.format_value import format_value


class ZuHeConverter(Converter):
    def __init__(self, name):
        self.name = name

    def convert(self, config, data):
        if data:
            try:
                data = data.decode().split(',')
                del data[0]
                logger.info(f"({self.name}姿态定位组合传感器)原始数据: {data}")
                dic = {}
                for index in config:
                    name = 'c' + str(index['serial_number'])
                    i = int(index['address'])
                    # 格式化数据
                    dic[name] = format_value(index, data[i])
                logger.info(f"{self.name}(姿态定位组合传感器)解析后数据：{data}")
                return dic
            except Exception as e:
                logger.error(e)
                return "error"
        else:
            return False
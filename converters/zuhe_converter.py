"""
@File  : cec21_converter.py
@Author: lee
@Date  : 2022/8/30/0030 14:42:02
@Desc  : 姿态定位组合传感器
"""
from logging_config import zuhe_converter as logger
from converter import Converter
from tools.format_value import format_value
from event_storage import EventStorage


class ZuHeConverter(Converter):
    def __init__(self, name):
        self.name = name
        self.__storager = EventStorage()

    def convert(self, config, data):
        if data:
            try:
                dic = None
                # logger.info(f"{self.name} : {data}")
                # print(data[0])
                # 判断byte数据以 $ 开头
                if data[0] == 36:
                    datas = data.decode().split('\r\n')
                    for dat in datas:
                        if dat.startswith("$INSPVAA"):
                            # 解析数据
                            dat = dat.split(',')
                            dat = dat[1:-1]
                            logger.info(f"{self.name}(姿态定位组合传感器)原始数据: {dat}")
                            dic = {}
                            if len(dat) == 11:
                                for index in config:
                                    name = 'c' + str(index['serial_number'])
                                    i = int(index['address'])
                                    # print(name, dat[i])
                                    # 格式化数据
                                    dic[name] = format_value(index, dat[i])
                                # logger.info(f"{self.name}(姿态定位组合传感器)解析后数据：{dic}")
                        elif dat.startswith("$GNGGA"):
                            # 存到redis
                            # 判断正常或异常
                            station_name = config[0]['station_name']
                            dic = {station_name: dat}
                            # logger.info(f"{self.name}(GNGGA数据):{dic}")
                            self.__storager.real_time_data_storage(dic)
                        else:
                            # 可能会有空格，所以什么也不做
                            pass
                    return dic
            except Exception as e:
                logger.error(f"{self.name}:{e}")
                return "error"
        else:
            return False
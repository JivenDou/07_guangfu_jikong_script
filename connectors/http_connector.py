#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2021/5/31 11:37
@desc: http连接器
"""

import json
import queue
import time
import traceback
import threading
import requests
from connector import Connector
from event_storage import EventStorage


class HttpConnector(Connector, threading.Thread):
    __master = 0
    _disConnectTime = 0

    def __init__(self, name, config, converter):
        super().__init__()
        self.__master = None
        self.__stopped = False
        self.__connected = False
        self.__save_frequency = config['save_frequency']  # 数据存储时间间隔
        self.setDaemon(True)
        self.setName(name)
        self.__converter = converter
        self.__storager = EventStorage()
        self.__command_queue = queue.Queue(50)
        self.__last_save_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)
        self.__command = self.__storager.get_command_info(name)

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connected = True
        command_list = json.loads(self.__command[0]['command'])
        while True:
            time.sleep(1)
            data = []
            for i in range(len(command_list)):
                url = command_list['url']
                postdata = command_list['data']
                try:
                    result = requests.post(url, data=json.dumps(postdata), timeout=0.1)
                    data = json.loads(result.text)
                except Exception as e:
                    print('shucai http connect error:{}'.format(str(e)))
                    time.sleep(5)
            self.command_polling(data, resend_times=5)

    def __connect(self):
        pass

    def __reconnect(self):
        pass

    def close(self):
        pass

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    def send_command(self, content):
        pass

    def command_polling(self, result, resend_times=None):
        format_data = self.__converter.convert(self.__data_point_config, result)
        if format_data:
            if format_data != "error" and format_data != 'pass':
                # 往redis存储数据
                self.__storager.real_time_data_storage(format_data)

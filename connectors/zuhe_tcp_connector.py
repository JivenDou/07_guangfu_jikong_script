"""
@Date  :2021/5/21/00219:10:57
@Desc  :姿态定位组合传感器
"""
import json
import time
import threading
import socket
import queue

from logging_config import zuhe_tcp_connector as logger
from connector import Connector
from event_storage import EventStorage


class ZuHeTcpConnector(Connector, threading.Thread):
    def __init__(self, name, config, converter):
        super().__init__()
        self.__sock = None
        self.__connected = False
        self.__stopped = False
        self.__size = 1024
        self.__ip = config['ip']
        self.__port = config['port']
        self.__converter = converter
        self.__storager = EventStorage()
        self.__save_frequency = config['save_frequency']
        self.__command_queue = queue.Queue(50)
        self.setName(name)
        self.__last_save_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)
        self.__command = self.__storager.get_command_info(name)

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connect()  # 建立socket连接
        self.__connected = True
        # 先发一次指令
        # if isinstance(self.__command, list):
        #     for i in self.__command:
        #         command_list = json.loads(i['command'])
        #         # print(command_list[0])
        #         self.send_command(command_list[0])
        while True:
            self.command_polling()
            time.sleep(self.__save_frequency)
            if self.__stopped:
                break

    # 建立socket连接
    def __connect(self):
        if self.__sock:
            self.__sock.close()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重用本地地址和端口
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        self.__sock.settimeout(180)  # 设置超时时间3mins
        try:
            self.__sock.connect((self.__ip, self.__port))
            logger.info(f'Connect to [{self.name}]:[{self.__ip}]:[{self.__port}] success !')
            self.__connected = True
        except Exception as e:
            logger.info(f'Connect to [{self.name}]:[{self.__ip}]:[{self.__port}] failed:{e} !!!')
            self.__connected = False
            self.__reconnect()

    # socket重连
    def __reconnect(self):
        while True:
            try:
                if self.__sock:
                    self.__sock.close()
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
                self.__sock.settimeout(180)  # 设置超时时间3mins
                self.__sock.connect((self.__ip, self.__port))
                self.__connected = True
                logger.info(f'Reconnect to [{self.name}]:[{self.__ip}]:[{self.__port}] success !')
                break
            except Exception as e:
                logger.info(
                    f'Reconnect to [{self.name}]:[{self.__ip}]:[{self.__port}] failed:{e} !!! Continue reconnect in 5s..')
                self.__connected = False
                time.sleep(5)

    def close(self):
        """Close the connection with the TCP Slave"""
        if self.__sock:
            self.__sock.close()
            self.__stopped = True
            self.__sock = None
            self.__connected = False

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    # 发送数据
    def send_command(self, command):
        if self.__sock:
            try:
                # print(command['instruct'])
                # com = bytes.fromhex(command['instruct'])
                com = command['instruct'].encode()
                self.__sock.send(com)
            except Exception as e:
                logger.info(f'Send command to [{self.name}]:[{self.__ip}]:[{self.__port}] error:{e}')

    def send_byte(self, byte_data):
        if self.__sock:
            try:
                # print(command['instruct'])
                # com = bytes.fromhex(command['instruct'])
                # print(byte_data)
                self.__sock.send(byte_data)
                return True
            except Exception as e:
                logger.info(f'Send command to [{self.name}]:[{self.__ip}]:[{self.__port}] error:{e}')
                return False
        else:
            return False

    # 监听数据
    def listen_data(self):
        try:
            recv_data = self.__sock.recv(self.__size)
            return recv_data
        except Exception as e:
            logger.error(f"{e}")
            return False

    # 发送并接收数据
    def exec_command(self, command):
        try:
            com = bytes.fromhex(command['instruct'])
            # com = command['instruct'].encode(encodings='utf-8')
            self.__sock.send(com)
            recv_data = self.__sock.recv(self.__size)
            return recv_data
        except Exception as e:
            logger.error(f"{e}")

    # 重复发送命令获取数据
    def command_polling(self, command_list=None):
        try:
            # 一直监听消息
            recv_data = self.listen_data()
            format_data = self.__converter.convert(self.__data_point_config, recv_data)
            # logger.info(f'{self.name} : {format_data}')
            if format_data and format_data != "error" and format_data != 'pass':
                self.__storager.real_time_data_storage(format_data)
        except Exception as e:
            logger.error(f'Other error occur [{self.name}]:[{self.__ip}]:[{self.__port}]:{e}')
            time.sleep(5)
            self.__reconnect()

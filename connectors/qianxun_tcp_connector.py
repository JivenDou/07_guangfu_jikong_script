"""
@Date  :2021/5/21/00219:10:57
@Desc  :向千寻服务器获取差分数据
"""
# import json
import time
import threading
import socket
import base64
# import queue

# from utility import Utility
import utility
from logging_config import qianxun_tcp_connector as logger
from connector import Connector
from event_storage import EventStorage


class QianXunConnector(Connector, threading.Thread):
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
        self.setName(name)
        self.__data_point_config = self.__storager.get_station_info(name)
        self.__userid = 'qxxtbq001'
        self.__password = '1edeed6'

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connect()  # 建立socket连接
        self.__connected = True
        # Regester
        self.__sock.send(b'GET /RTCM32_GGB HTTP/1.0\r\n')
        self.__sock.send(b'User-Agent: NTRIP GNSSInternetRadio/1.4.10\r\n')
        self.__sock.send(b'Authorization: Basic ' + base64.encodebytes((self.__userid + ':' + self.__password).encode()) + b'\r\n\r\n')
        # m = b'Authorization: Basic ' + base64.encodebytes((self.__userid + ':' + self.__password).encode()) + b'\r\n\r\n'
        # print(m.decode())
        while True:
            # 从redis获取GNGGA数据
            station_names = ["A_ZuHe", "B_ZuHe", "C_ZuHe", "D_ZuHe"]
            command_dic = self.__storager.memoryStorage.get_value(station_names)
            command = None
            # 从四个中获取一条GNGGA数据
            # print(command_dic)
            for key in command_dic:
                if command_dic[key]:
                    command = command_dic[key]
                    break
            if command:
                self.command_polling(command=command)
            time.sleep(self.__save_frequency)

            if self.__stopped:
                break

    # 建立socket连接
    def __connect(self):
        if self.__sock:
            self.__sock.close()
        # self.__sock = socket.socket()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重用本地地址和端口
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        self.__sock.settimeout(10)  # 设置超时时间10s
        try:
            self.__sock.connect((self.__ip, self.__port))
            # self.__sock.connect(('ntrip.qxwz.com', 8002))
            logger.info(f'Connect to [{self.name}]:[{self.__ip}]:[{self.__port}] success !')
            # data = self.listen_data()
            # print("data:", data)
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
                # self.__sock = socket.socket()
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
                self.__sock.settimeout(10)  # 设置超时时间10s
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
                com = command.encode()
                # print(com + b'\r\n')
                # # Regester
                # self.__sock.send(b'GET /RTCM32_GGB HTTP/1.0\r\n')
                # self.__sock.send(b'User-Agent: NTRIP GNSSInternetRadio/1.4.10\r\n')
                # self.__sock.send(b'Authorization: Basic ' + base64.encodebytes((self.__userid + ':' + self.__password).encode()) + b'\r\n\r\n')
                self.__sock.send(com + b'\r\n')
            except Exception as e:
                logger.info(f'Send command to [{self.name}]:[{self.__ip}]:[{self.__port}] error:"{e}"')

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
    def command_polling(self, command=None):
        if command:
            try:
                # 发送命令
                # print("======", command)
                self.send_command(command)
                # 监听消息
                recv_data = self.listen_data()
                # print("recv_data:", recv_data)
                # 判空
                if recv_data and recv_data != b' ' and recv_data != b'ICY 200 OK\r\n\r\n':
                    # 获取四个传感器连接对象，对设备分发差分数据
                    a_zuhe = utility.Utility.available_connectors["A_ZuHe"]
                    b_zuhe = utility.Utility.available_connectors["B_ZuHe"]
                    c_zuhe = utility.Utility.available_connectors["C_ZuHe"]
                    d_zuhe = utility.Utility.available_connectors["D_ZuHe"]
                    a_zuhe.send_byte(recv_data)
                    b_zuhe.send_byte(recv_data)
                    c_zuhe.send_byte(recv_data)
                    d_zuhe.send_byte(recv_data)

                    # if a_zuhe.send_byte(recv_data):
                        # logger.info(f'a_zuhe send success')
                    # if b_zuhe.send_byte(recv_data):
                        # logger.info(f'b_zuhe send success')
                    # if c_zuhe.send_byte(recv_data):
                        # logger.info(f'c_zuhe send success')
                    # if d_zuhe.send_byte(recv_data):
                        # logger.info(f'd_zuhe send success')

            except Exception as e:
                logger.error(f'Other error occur [{self.name}]:[{self.__ip}]:[{self.__port}]:{e}')
                time.sleep(5)
                self.__reconnect()

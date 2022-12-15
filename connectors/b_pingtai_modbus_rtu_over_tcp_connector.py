import json
import threading
import queue
import time
from modbus_tk import modbus_rtu_over_tcp
from connector import Connector
from event_storage import EventStorage
from logging_config import b_pingtai_modbus_connector as logger


class BPingTaiModbusRtuOverTcpConnector(Connector, threading.Thread):
    def __init__(self, name, config, converter):
        super().__init__()
        self._master = None
        self.__stopped = False
        self._connected = False
        self._ip = config['ip']  # ip
        self._port = config['port']  # 端口
        self._save_frequency = config['save_frequency']  # 数据存储时间间隔
        self.setDaemon(True)
        self.setName(name)
        self.__converter = converter
        self.__storager = EventStorage()
        self.__command_queue = queue.Queue(500)
        self.__last_save_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)
        self._name = name
        self.run_time = 0
        self._command = self.__storager.get_command_info(name)

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self._connect()
        self._connected = True
        while True:
            if isinstance(self._command, list):
                for i in self._command:
                    command_list = json.loads(i['command'])
                    self.command_polling(command_list, resend_times=5)
                    time.sleep(self._save_frequency)
            # time.sleep(1)
            if self.__stopped:
                break

    def _connect(self):
        try:
            self._master = modbus_rtu_over_tcp.RtuOverTcpMaster(host=self._ip, port=self._port)
            logger.info(f"{self._ip}:{self._port} connect success!")
        except Exception as e:
            logger.error(f'Error in modbus_tcp_connector.__connect: {repr(e)}')
            self._connected = False
            self._reconnect()

    def _reconnect(self):
        while True:
            try:
                self._master = modbus_rtu_over_tcp.RtuOverTcpMaster(host=self._ip, port=self._port)
                logger.error('client start connect to host/port:{}'.format(self._port))
                break
            except ConnectionRefusedError:
                logger.error('modbus server refused or not started, reconnect to server in 5s .... host/port:{}'.format(
                    self._port))
                time.sleep(5)
            except Exception as e:
                logger.error('do connect error:{}'.format(str(e)))
                time.sleep(5)

    def close(self):
        pass

    def get_name(self):
        return self.name

    def is_connected(self):
        return self._connected

    def send_command(self, command):
        # command = {'device_id': 1, 'start_addr': 0, 'output_value': [0, 0, 0, 0], 'function_code': 15}
        # print(f"[send_command] {command}")
        try:
            result = None
            if isinstance(command, dict):
                result = self.exec_command(command)
            elif isinstance(command, list):
                for each in command:
                    result = self.exec_command(each)
            return result
        except Exception as e:
            print(f"[ModbusTcpConnector][send_command] error: {e}")
            return None

    def exec_command(self, command):

        if isinstance(command, str):
            command = json.loads(command)
        device_id = int(command['device_id'])
        function_code = int(command['function_code'])
        start_addr = int(command['start_addr'])
        if function_code in (1, 2, 3, 4):
            # 读寄存器
            length = int(command['length'])
            try:
                self._master.set_timeout(3.0)  # modbus读取数据超时时间设置
                self._master.set_verbose(True)
                # print(device_id, ' ', function_code, " ", start_addr, " ", length)
                receive_data = self._master.execute(device_id, function_code, start_addr, length)
                # print("receive_data:", receive_data)
                datadict = {}
                for i in range(len(receive_data)):
                    addr = start_addr + i
                    datadict[addr] = receive_data[i]
                result = [device_id, datadict]
                return result
            except Exception as e:
                logger.error(f'An error occurred while executing the read register command:{e}')
                # self._reconnect()
        elif function_code in (5, 6, 15, 16):
            # 写寄存器
            output_value = command['output_value']
            try:
                self._master.set_timeout(10.0)
                self._master.set_verbose(True)
                data = self._master.execute(device_id, function_code, start_addr, output_value=output_value)
                # print("data = ", data)
                # data = (0, 65280) or (0, 0)
                result = False
                if function_code == 5 and "res" in command.keys():
                    res = command["res"]
                    if start_addr == data[0] and res == data[1]:
                        result = True
                return result
            except Exception as e:
                logger.error(f'An error occurred while executing the write register command:{e}')
        else:
            logger.error(f'Unsupported function code.')

    def command_polling(self, command_list, resend_times=None):
        # msg = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        for i in range(len(command_list)):
            command_item = command_list[i]
            # time.sleep(1)
            if not self.__command_queue.empty():
                write_command = self.__command_queue.get()  # 写命令来自数组
                try:
                    res = self.exec_command(command=write_command)
                    logger.info(res)
                except Exception as e:
                    logger.error("modbus_rtu,write[ERROR]:" + str(e))
            else:
                try:
                    time.sleep(0.05)
                    result = self.exec_command(command=command_item)
                    format_data = None
                    # print(self.__data_point_config)
                    # print(result)
                    if result:
                        format_data = self.__converter.convert(self.__data_point_config, result)
                    logger.info(f'{self.name}/device_id={result[0]}: {format_data}')
                    if format_data and format_data != "error" and format_data != 'pass':
                        # 往redis存储数据
                        self.__storager.real_time_data_storage(format_data)
                except Exception as e:
                    logger.error(f"{repr(e)}")

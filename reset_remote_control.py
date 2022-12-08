#!/usr/bin/env python
# encoding: utf-8
"""
@CreateTime: 2022/09/23 14:20
@Author: lxc
@LastEditTime: 
@Desctiption: 远程开关量模块的复位逻辑
"""



from log import OutPutLog
from event_storage import EventStorage
import time
from utility import Utility
from datetime import datetime


class ResetRemoteControl:
    def __init__(self):
        self._log = OutPutLog()
        self._storage = EventStorage()
        self._now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self):

        # c411：主发电机系统工作模式	0：本地模式，1：遥控模式，2：自动模式
        # c432：应急发电机系统工作模式	0：本地模式，1：遥控模式，2：自动模式
        point_list = ["c411", "c432"]

        run_time = 0
        while True:
            this_time = time.time()
            if this_time - run_time > 10:
                run_time = this_time

                real_data_dict = self._storage.get_real_data(point_list)
                zfdj_system = real_data_dict["c411"]
                yjfdj_system = real_data_dict["c432"]


                print(self._now, "zfdj_system = ,", zfdj_system)
                if zfdj_system is not None:
                    if int(zfdj_system) != 2:
                        command = {"device_id": 1, "start_addr": 3, "output_value": 0, "function_code": 5, "res": 0}
                        self.send_command(command)


                if yjfdj_system is not None:
                    if int(yjfdj_system) != 2:
                        command = {"device_id": 1, "start_addr": 4, "output_value": 0, "function_code": 5, "res": 0}
                        self.send_command(command)




    def send_command(self, command):
        """
        发送指令
        :return:
        """
        print(f"{self._now} 开始发送指令")
        station_name = "remote_control"
        commend_result = Utility.available_connectors[station_name].send_command(command)
        if commend_result is False:
            print(f"{self._now} 指令发送失败！ {command}")
        else:
            print(f"{self._now} 指令发送成功！ {command}")
















        # remote_control_status = 1       # 远程开关量的状态  0:断开， 1:闭合
        #
        # if remote_control_status == 1:
        #     # 远程开关量模块闭合
        #     fdj_status = 1          # 发电机运行状态 0：未运行， 1：运行
        #
        #     if fdj_status == 0:
        #         # 发电机未运行
        #         work_status = 0     # 发电机工作模式    0：本地模式，1：遥控模式，2：自动模式



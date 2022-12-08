import time
from event_storage import EventStorage
from log import OutPutLog
from datetime import datetime, timedelta


class Alarm:
    def __init__(self):
        self._storage = EventStorage()
        self._save_frequency = 5
        self._last_save_time = 0
        self._log = OutPutLog()

    def get_real_time_data(self):
        """
        :return: data_dict {'c1': '064', 'c2': '0.1', 'c3': '20.3', 'c4': '43.2', 'c5': '1025.1', 'c6': '0.25', 'c81': '29.823', 'c82': '104.507', 'c83': '253.153'...}
        """
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        # print(point_info)
        keys_list = []
        for index in point_info:
            keys_list.append('c' + str(index['serial_number']))
        data_dict = self._storage.memoryStorage.get_value(keys_list)
        # print(data_dict)
        return data_dict

    def get_point_table(self):
        """
        获取所有点的点表，并增加alarm_status属性
        :return: point_info 字典组成的列表
        """
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        for obj in point_info:
            obj['alarm_status'] = 0
        return point_info

    def update_point_table(self, point_info):
        """
        更新点表，主要更新报警上限和报警下限
        :param point_info: 更新前的点表
        :return: 更新后的点表
        """
        new = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        for i in range(0, len(new)):
            point_info[i]['alarm_low_limit'] = new[i]['alarm_low_limit']
            point_info[i]['alarm_up_limit'] = new[i]['alarm_up_limit']

    # 越限报警
    def overrun_alarm(self):
        self._log.info('[overrun_alarm] - Over run alarm module is running!')
        try:
            point_info = self.get_point_table()
            while 1:
                self.update_point_table(point_info)
                # print(time.time(), point_info[0]['alarm_low_limit'], point_info[0]['alarm_up_limit'])
                data_dict = self.get_real_time_data()
                # print(data_dict['c1'])
                for index in point_info:
                    key = 'c' + str(index['serial_number'])
                    # print('addr = ', addr, 'addr type = ', type(addr))
                    if data_dict[key]:  # 数据不为空且报警状态为零
                        data_dict[key] = float(data_dict[key])
                        if index['alarm_low_limit'] is None or index['alarm_up_limit'] is None:  # 未设置报警限值
                            continue
                        elif index['alarm_low_limit'] <= data_dict[key] <= index['alarm_up_limit']:  # 在合理范围内
                            index['alarm_status'] = 0
                        else:  # 数据越限
                            if index['alarm_status'] == 0:  # alarm_status == 0：表示第一次报警，存储报警信息
                                alarm_unit = {'name': "'" + key + "'", 'data': data_dict[key]}
                                table_name = "alarm_data_tbl"  # 报警存储表名，可以通过配置文件配置
                                alarm_time = time.strftime("%Y-%m-%d %H:%M:%S")
                                self._log.debug('[overrun_alarm] - ' + repr(alarm_unit))
                                self._storage.hardDiskStorage.insert_column_many(table_name, alarm_time, alarm_unit)
                                index['alarm_status'] = 1
                            elif index['alarm_status'] == 1:  # alarm_status == 1：表示本次报警期间非第一次检测的越限
                                continue
                time.sleep(1)
        except Exception as e:
            msg = str(time.strftime("%Y-%m-%d %H:%M:%M"))
            print(f'{msg}: error in overrun_alarm: {e}')

    def overrun_alarm_storage(self, table_name, save_time, item):
        pass

    # 变位报警
    def displacement_alarm(self):
        self._log.info('[displacement_alarm] - Displacement alarm module is running!')
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)

        keys_list = []
        for index in point_info:
            keys_list.append('c' + str(index['serial_number']))
        last_data_dict = self._storage.memoryStorage.get_value(keys_list)

        while 1:
            now_data_dict = self._storage.memoryStorage.get_value(keys_list)
            # print(now_data_dict)
            for index in point_info:
                key = 'c' + str(index['serial_number'])
                if index['signal_type'] == 'Switch' and now_data_dict[key]:
                    if now_data_dict[key] != last_data_dict[key]:
                        self._log.info(repr(now_data_dict[key]) + repr(last_data_dict[key]))
                    else:
                        pass
            last_data_dict = now_data_dict
            self._log.info(last_data_dict)
            time.sleep(1)

    def displacement_alarm_storage(self):
        pass


    def moxa_e1210_alarm(self):
        """开关量综合报警的提示"""
        point_list = ["c365", "c367", "c368", "c371", "c372", "c373", "c374", "c375", "c376", "c377"]
        real_data_dict = self._storage.get_real_data(point_list)
        # real_data_dict = {'c365': '0', 'c367': '0', 'c368': '1', 'c371': '0', 'c372': '0', 'c373': '0', 'c374': '0', 'c375': '0', 'c376': '1', 'c377': '0'}
        alarm_time = datetime.now()
        alarm_time_limit = (alarm_time+timedelta(minutes=-30)).strftime("%Y-%m-%d %H:%M:%S")
        
        for serial_number,value in real_data_dict.items():
            if value and int(value) == 1:
                select_sql = f"SELECT serial_number FROM alarm_moxa_e1210 WHERE serial_number=\'{serial_number}\' AND update_time>\'{alarm_time_limit}\';"
                if not self._storage.execute_sql(select_sql):
                    insert_sql = f"INSERT INTO alarm_moxa_e1210 (`create_time`, `update_time`, `serial_number`) VALUES (\'{alarm_time}\', \'{alarm_time}\', \'{serial_number}\');"
                    self._storage.execute_update_sql(insert_sql)
                else:
                    update_sql = f"UPDATE alarm_moxa_e1210 SET update_time=\'{alarm_time}\' WHERE serial_number=\'{serial_number}\' AND update_time>\'{alarm_time_limit}\';"
                    self._storage.execute_update_sql(update_sql)
        


if __name__ == '__main__':
    alarm = Alarm()
    alarm.overrun_alarm()

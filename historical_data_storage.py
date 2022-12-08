import json
import threading
from event_storage import EventStorage
import time
from logging_config import general as logger


class HistoricalDataStorage(threading.Thread):
    def __init__(self):
        super(HistoricalDataStorage, self).__init__()
        self._storage = EventStorage()

    # 历史存储主函数
    def run(self):
        logger.info('Historical data storage module is running!')
        station_info = self._storage.hardDiskStorage.get_connectors()  # 获取所有站点信息

        all_devices = []
        for item in station_info:
            station_name = item['station_name']  # 站点名称
            connector_config = json.loads(item['connector_config'])  # 加载json格式connector_config参数
            save_frequency = connector_config['save_frequency']  # 获取存储频率
            devices_each_station = self._storage.hardDiskStorage.get_device_name_by_station_name(station_name)  # 根据站点名称获取设备列表
            # print(devices_each_station)
            for i in devices_each_station:
                temp_dict = {}
                # 获取每个设备所有点的serial_number,转换为键列表
                device_name = i['device_name']
                data_point_each_decive = self._storage.hardDiskStorage.get_data_point_by_device_name(device_name)  # 根据设备名称获取设备点表

                serial_number_list = []
                for item in data_point_each_decive:
                    serial_number = 'c' + str(item['serial_number'])
                    serial_number_list.append(serial_number)

                temp_dict['device_name'] = device_name
                temp_dict['save_frequency'] = save_frequency
                temp_dict['serial_number_list'] = serial_number_list
                temp_dict['last_save_time'] = 0

                all_devices.append(temp_dict)
        while 1:
            time.sleep(0.2)
            for item in all_devices:
                save_frequency = item['save_frequency']
                last_save_time = item['last_save_time']
                now_time = time.time()

                serial_number_list = item['serial_number_list']
                real_time_data = self._storage.memoryStorage.get_value(serial_number_list)  # 根据键列表查询实时数据库
                if now_time - last_save_time >= save_frequency:
                    item['last_save_time'] = now_time
                    save_time = int(now_time) - int(now_time) % save_frequency
                    save_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(save_time))
                    # print(real_time_data)
                    flag = False  # 是否允许存储标志位
                    for key in real_time_data:
                        # 值全部为空，不允许存储
                        if real_time_data[key]:
                            flag = True
                            break
                    if flag:
                        for key in real_time_data:  # redis值为None的
                            if real_time_data[key] is None:  # redis数据库未存储此值
                                real_time_data[key] = 'null'
                            if real_time_data[key] == '':  # redis存储的为空值
                                real_time_data[key] = 'null'
                        table_name = "table_" + str(item['device_name'])  # 根据站名计算表名
                        # print(table_name)
                        logger.debug(f"{table_name} <- {real_time_data}")
                        # print(table_name)
                        self._storage.hardDiskStorage.insert_column_many(table_name, save_time, real_time_data)


if __name__ == '__main__':
    historicalDataStorage = HistoricalDataStorage()
    historicalDataStorage.run()

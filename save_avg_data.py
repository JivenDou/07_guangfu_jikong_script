import threading
import json
import time
from datetime import datetime
from datetime import timedelta
from logging_config import general as logger
from event_storage import EventStorage


class SaveAvgData(threading.Thread):
    def __init__(self):
        super(SaveAvgData, self).__init__()
        self._storage = EventStorage()

    def run(self):
        logger.info('Save Avg Data is running!')
        # 获取设置了avg_sec的串口信息
        sql = "SELECT station_name,avg_sec FROM `station_info_tbl` WHERE avg_sec IS NOT NULL;"
        station_names = self._storage.hardDiskStorage.execute_sql(sql)
        device_infos = []
        # 遍历所有串口服务器
        for s_item in station_names:
            # 获取串口设备名和保存平均几秒
            station_name = s_item['station_name']
            avg_sec = s_item['avg_sec']
            # 获取点表中需要存平均数的设备
            sql = f"SELECT DISTINCT device_name FROM data_point_tbl WHERE station_name='{station_name}';"
            device_names = self._storage.hardDiskStorage.execute_sql(sql)
            device_names = [i['device_name'] for i in device_names]
            device_infos.append({'avg_sec': avg_sec, 'device_names': device_names, 'last_save_time': 0})
        # print(device_infos)
        while True:
            time.sleep(0.2)
            for device_info in device_infos:
                # device_info : {'avg_sec': 10, 'device_names': ['PZ72_DE_C_4', 'PZ72_DE_C_5', 'CR1000X_2'], 'last_save_time': 0}
                avg_sec = device_info['avg_sec']
                device_names = device_info['device_names']
                last_save_time = device_info['last_save_time']
                now_time = time.time()
                # 若现在距离上一次存过了avg_sec秒
                if now_time - last_save_time >= avg_sec:
                    # 记录本次时间
                    device_info['last_save_time'] = int(now_time)
                    save_time = int(now_time) - int(now_time) % avg_sec
                    save_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(save_time))
                    # print(save_time)
                    # print(avg_sec, device_names)
                    # 遍历所有设备
                    for device_name in device_names:
                        new_table_name = f"copy_table_{device_name}"
                        # 获取平均的数据
                        datas = self.get_avg_datas(device_name, avg_sec)
                        # print(datas)
                        # 判断如果都是空值就不插入了
                        # datas：{'c1507': None, 'c1508': None, 'c1509': None, 'c1510': None, 'c1511': None}
                        flag = False
                        for data in datas.values():
                            if data is not None:
                                flag = True
                                break
                        # 将数据插入新表
                        if flag:
                            points = [i for i in datas.keys()]
                            value = ['NULL' if i is None else str(i) for i in datas.values()]
                            sql = f"INSERT INTO {new_table_name}(times,{','.join(points)}) VALUES('{save_time}',{','.join(value)})"
                            # print(sql)
                            self._storage.hardDiskStorage.execute_sql(sql)

    def get_avg_datas(self, device_name, avg_sec):
        """
        获取平均的数据
        :param device_name: PZ72_DE_C_4
        :param avg_sec: 10
        :return: datas
        """
        # 设置新旧表名
        old_table_name = f"table_{device_name}"
        # print(device_name, old_table_name, new_table_name)
        # 组装各点的sql语句
        sql = f"SELECT serial_number,round FROM data_point_tbl WHERE device_name='{device_name}';"
        serial_numbers = self._storage.hardDiskStorage.execute_sql(sql)
        points = [f"ROUND(AVG(c{i['serial_number']}),2) c{i['serial_number']}" if i['round'] is None else
                  f"ROUND(AVG(c{i['serial_number']}),{i['round']}) c{i['serial_number']}" for i in serial_numbers]
        # 获取时间
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        before_time = datetime.now() + timedelta(seconds=-avg_sec)
        before_time = before_time.strftime('%Y-%m-%d %H:%M:%S')
        # print(now_time, before_time)
        # 获取数据信息
        sql = f"SELECT {','.join(points)} FROM `{old_table_name}` WHERE times<='{now_time}' AND times>='{before_time}';"
        datas = self._storage.hardDiskStorage.execute_sql(sql)[0]
        for d in datas:  # 将decimal转float
            if not isinstance(datas[d], float) and datas[d] is not None:
                datas[d] = float(datas[d])
        return datas


if __name__ == '__main__':
    saveAvgData = SaveAvgData()
    saveAvgData.run()

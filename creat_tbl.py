#!/usr/bin/env python
# encoding: utf-8
"""
@CreateTime: 2022/06/27 09:28
@Author: lxc
@LastEditTime: 
@Desctiption:
"""



from event_storage import EventStorage
from log import OutPutLog



save_log = OutPutLog()
operate_mysql = EventStorage()


def creatr_table():
    # select_all_device_sql = "SELECT DISTINCT(device_name) FROM `data_point_tbl`;"
    select_all_device_sql = "SELECT DISTINCT(device_name) FROM `data_point_tbl`;"
    all_device = operate_mysql.execute_sql(select_all_device_sql)
    num = 1
    for device in all_device:
        device_name = device["device_name"]
        table_name = "table_" + device_name
        create_sql = f"CREATE TABLE `{table_name}` (`id` bigint(20) NOT NULL AUTO_INCREMENT,`times` datetime NOT NULL,"


        select_point_sql = f"SELECT serial_number,io_point_name,storage_type FROM `data_point_tbl` WHERE device_name=\'{device_name}\';"
        all_point = operate_mysql.execute_sql(select_point_sql)
        for point in all_point:
            serial_number = "c" + str(point["serial_number"])
            io_point_name = point["io_point_name"]
            storage_type = point["storage_type"]
            create_sql = create_sql + f"`{serial_number}` {storage_type} DEFAULT NULL comment '{io_point_name}',"

        create_sql = create_sql + "`is_send` tinyint(1) NOT NULL DEFAULT '0' comment '上传标志'," \
                                  "PRIMARY KEY (`id`),KEY `times` (`times`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        print(num, create_sql)
        num += 1
        res = operate_mysql.execute_sql(create_sql)

        print(res, table_name)
        # save_log.info(f"{res, device_name}")
        # save_log.info(create_sql)


creatr_table()





"""
CREATE TABLE `table_dbqycfpffj_electric` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `times` datetime NOT NULL,
  `c631` float DEFAULT NULL,
  `c632` float DEFAULT NULL,
  `c633` float DEFAULT NULL,
  `c634` float DEFAULT NULL,
  `c635` float DEFAULT NULL,
  `c636` float DEFAULT NULL,
  `c637` float DEFAULT NULL,
  `c638` float DEFAULT NULL,
  `c639` float DEFAULT NULL,
  `c640` float DEFAULT NULL,
  `is_send` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `times` (`times`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
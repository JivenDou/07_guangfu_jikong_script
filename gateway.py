#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@desc: 连接器：可读，可写
"""

import time
import threading
import os
from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic import response
from event_storage import EventStorage
from utility import Utility
from historical_data_storage import HistoricalDataStorage
from save_avg_data import SaveAvgData
from alarm import Alarm
from reset_remote_control import ResetRemoteControl
from reset_remote_control import ResetRemoteControl
from logging_config import LOGGING_CONFIG
import logging.config


app = Sanic(__name__)
CORS(app)

# logging config
logging.config.dictConfig(LOGGING_CONFIG)
handlers = LOGGING_CONFIG['handlers']
for handler in handlers:
    item = handlers[handler]
    if 'filename' in item:
        filename = item['filename']
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
# --------------------------
gateway_storage = EventStorage()
connector_config = gateway_storage.get_connector_config()
Utility.start_connectors(connector_config)


@app.route('/readRealText', methods=['POST'])
async def read_point_data_text(request):
    list = request.json['pointList']
    dict = gateway_storage.get_real_data(list)
    # print(dict)
    point_list = gateway_storage.get_point_info(list)
    data_list = {}
    for info in point_list:
        data_list[info['io_point_name']] = str(dict["c"+str(info['serial_number'])]) + " " +str(info['unit'])
    return response.json(dict)


# @app.route('/readReal', methods=['POST'])
# async def read_point_data(request):
#     list = request.json['pointList']
#     dict = gateway_storage.get_real_data(list)
#     '''
#     data_list = gateway_storage.get_point_info(list)
#     for info in data_list:
#         info['value'] = dict["c"+str(info['serial_number'])]
#     '''
#     return response.json(dict)
#
#
# @app.route('/api', methods=['POST'])
# async def read_statistics_data(request):
#     if len(request.json) > 0:
#         list = []
#         for index in range(len(request.json)):
#             api_object = request.json[index]['apiObject']
#             parameter = request.json[index]['parameter']
#             api = ApiContext()
#             api.set_api_object(api_object)
#             result = api.operation(parameter)
#             list.append(result)
#         data_json = Utility.data_encoder(list)
#         return response.text(data_json)
#
# @app.route('/write',methods=['POST'])
# async def write_data(request):
#     t1 = time.time()
#     station_name = request.json["station_name"]
#     command = request.json["command"]
#     try:
#         result = Utility.available_connectors[station_name].send_command(command)
#         return response.json({'message': result})
#     except Exception as e:
#         print(station_name+"write[ERROR]:" + str(e))
#         return response.json({'message': result})


if __name__ == "__main__":
    # 存历史数据
    # HistoricalDataStorage().start()
    # 存平均值数据
    # SaveAvgData().start()
    app.run(host="0.0.0.0", port=18080, workers=1)

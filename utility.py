import importlib
import json
import datetime
import connectors
import converters

# name = "Test"
# zz = connectors.modbus_connector.Test()
# zz.f()


class Utility:
    loaded_connector_module = {}
    loaded_converter_module = {}
    available_connectors = {}

    @staticmethod
    def import_connector_module(configs):
        for config in configs:
            module_name = "connectors." + config['connector_module']
            class_name = config['connector']
            if Utility.loaded_connector_module.get(class_name) is None:
                extension_class = getattr(eval(module_name), class_name)
                Utility.loaded_connector_module[class_name] = extension_class
        return Utility.loaded_connector_module

    @staticmethod
    def import_converter_module(configs):
        for config in configs:
            module_name = "converters." + config['converter_module']
            class_name = config['converter']
            if Utility.loaded_converter_module.get(class_name) is None:
                extension_class = getattr(eval(module_name), class_name)
                Utility.loaded_converter_module[class_name] = extension_class
        return Utility.loaded_converter_module

    @staticmethod
    def start_connectors(configs):
        connectors = Utility.import_connector_module(configs)
        converters = Utility.import_converter_module(configs)
        for config in configs:
            connector_config = config['connector_config']   # {'ip': '127.0.0.1', 'port': 502, 'deviceID': 1, 'save_frequency': 5, 'alarm_save_frequency': 15}
            name = config['station_name']                   # 'sct003'
            converter = converters[config['converter']](name)
            connector = connectors[config['connector']](name, connector_config, converter)
            Utility.available_connectors[name] = connector
            connector.open()

    @staticmethod
    def data_encoder(data_list):
        data_json = json.dumps(data_list, cls=DateEncoder)
        return data_json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

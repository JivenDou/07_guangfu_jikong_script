import json
import os
from logging_config import general as logger
import sys
from AES_crypt import decrypt


class Configuration:
    def __init__(self, path='config.json'):
        self.path = path
        try:
            with open(self.path) as json_file:
                self.config = json.load(json_file)
        except FileNotFoundError as e:
            logger.error(f"当前路径：{os.getcwd()}无法找到配置文件:{e}")
            input("按任意键退出！")
            sys.exit()

    def get_config(self):
        """"读取配置"""
        return self.config
        # 解密密码和序列号
        # config['hardDiskdataBase']['password'] = DesEncrypt(
        #     config['hardDiskdataBase']['password']).decode('utf-8')
        # config['code'] = DesEncrypt(config['code']).decode('utf-8')

    def set_config(self, **kwargs):
        config = self.get_config()
        for k, v in kwargs.items():
            k = k.split('.')
            len_k = len(k)
            try:
                if len_k == 1:
                    config[k[0]] = v
                elif len_k == 2:
                    config[k[0]][k[1]] = v
                elif len_k == 3:
                    config[k[0]][k[1]][k[2]] = v
            except KeyError as e:
                print("键名错误", e)
                return False
        with open(self.path, "w") as f:
            json.dump(config, f)
        return True

    def add_device(self):
        pass

    def delete_device(self):
        pass

    def updata_device(self):
        pass


if __name__ == '__main__':
    # config = Configuration("./config.json")
    # dict = {"hardDiskdataBase.username": "zz", "hardDiskdataBase.ip": "127.0.0.1"}
    # config.set_config(**dict)
    config = Configuration()
    res = config.set_config(**{"activation_code": "local_code"})
    print(res)

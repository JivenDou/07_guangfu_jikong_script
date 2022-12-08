import redis


class MemoryStorage():
    def __init__(self, config):
        self.ip = config['ip']
        self.port = config['port']
        self.conn = redis.StrictRedis(host=self.ip, port=self.port, db=0, decode_responses=True)

    def connected(self):
        pass

    def set_value(self, data_dict):
        try:
            pipe = self.conn.pipeline(transaction=True)
            for key_name in data_dict.keys():
                pipe.set(key_name, data_dict[key_name], ex=300)  # redis过期时间5mines
            pipe.execute()
        except Exception as e:
            print(e)
            return e
        else:
            return True

    def get_value(self, keys):
        dict = {}
        try:
            pipe = self.conn.pipeline(transaction=True)
            for index in range(len(keys)):
                pipe.get(keys[index])
            result = pipe.execute()
            for index in range(len(keys)):
                dict[keys[index]] = result[index]
            return dict
        except Exception as e:
            return e

    def is_connected(self):
        pass

    def re_connected(self):
        pass

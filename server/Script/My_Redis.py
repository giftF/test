import redis
from config.configRedis import ConfigRedis

class My_redis(object):
    def __init__(self):
        '''

        :param host: redis服务器ip
        :param port: redis服务端口
        :param password: 密码
        '''
        c_r = ConfigRedis()
        # self.pool = redis.ConnectionPool(host=c_r.host, port=c_r.port, password=c_r.password)
        self.pool = redis.ConnectionPool(host=c_r.host, port=c_r.port)
        self.r = redis.Redis(connection_pool=self.pool)
        keys = self.r.keys()
        for i in keys:
            self.r.delete(i)

    def set(self, key, value):
        '''
        输入值
        :param key:
        :param value:
        :return:
        '''
        self.r.set(key, value)

    def setex(self, key, value, t):
        '''
        输入值，有过期时间（秒）
        :param key:
        :param value:
        :param t: 过期时间，秒
        :return:
        '''
        self.r.setex(key, value, t)

    def psetex(self, key, t, value):
        '''
        输入值，有过期时间（毫秒）
        :param key:
        :param t:
        :param value:
        :return:
        '''
        self.r.psetex(key, t, value)

    def hset(self, name, key, value):
        '''
        Hash储存类似于一个dict
        :param name:
        :param key:
        :param value:
        :return:
        '''
        self.r.hset(name, key, value)

    def hget(self, name, key):
        '''
        Hash取值
        :param name:
        :param key:
        :return:
        '''
        return self.r.hget(name, key).decode('UTF-8')

    def hgetall(self, name):
        '''
        Hash取所有值
        :param name:
        :return:
        '''
        return self.r.hgetall(name).decode('UTF-8')

    def get(self, key):
        '''
        取值
        :param key:
        :return:
        '''
        return self.r.get(key).decode('UTF-8')

    def delete(self, name):
        '''
        删除内容
        :param name:
        :return:
        '''
        self.r.delete(name)

    def keys(self):
        '''
        获取当前所有key
        :return:
        '''
        return self.r.keys()

    def clean(self):
        keys = self.r.keys()
        for i in keys:
            if 'test_' in i.decode('UTF-8'):
                self.r.delete(i)
from pymongo import MongoClient
import pymongo
from numpy.random import randint


def ConnectMongoProTable(host, port, user=None):
    """

    连接远程MongoDB数据库，加上验证用户权限
    :param host:    数据库的ip-address
    :param port:    开放连接的端口
    :param user:    dict 用户名和密码
    :return:    数据库对象
    """
    client = MongoClient(host, port)
    db = client.proxyipDB
    if user is None:
        pass
    else:
        user = dict(user)
        db.authenticate(user['username'], user['password'])
    return db


class MymongoControl:
    collection = None

    def __init__(self, collection):
        """

        :param database: 数据库表名
        """
        if not isinstance(collection, pymongo.collection.Collection):
            raise AttributeError('传入的参数不是数据库名!')
        self.collection = collection

    def InsertData(self, *data):
        """
        封装pymong的增加数据函数，增加一条数据和增加多条数据都使用此函数，增加一条数据只需要传入一个dict，
        增加多条数据只需要传入一个由dict组成的list
        :param data:    要增加的数据
        :return:   成功返回true失败返回false
        """
        if len(data) > 1:
            raise AttributeError('填入数据有误！请填入一条的dict或者多条数据组成的list')
        _data = data[0]
        if isinstance(_data, dict):
            try:
                self.collection.insert_one(_data)
                return True
            except:
                return False
        elif isinstance(_data, list):
            try:
                self.collection.insert_many(_data, ordered=False)
            except:
                return True
        else:
            raise AttributeError('传入要增加的数据的格式错误!')

    def DeleteData(self, keyword):
        """
        封装pymongo删除数据函数
        :param keyword:     要删除的数据的关键字
        :return:    成功返回true失败返回false
        """
        if isinstance(keyword, dict):
            try:
                self.collection.delete_one(keyword)
            except:
                return False
            else:
                return True
        elif isinstance(keyword, list):
            try:
                for i in keyword:
                    self.collection.delete_one({'ip:port': i['ip:port']})
            except:
                return False
            else:
                return True
        else:
            raise AttributeError('传入参数有误，请传入dict类型')

    def QueryAllData(self):
        """
        查询所有数据拼接成列表
        :return: 返回所有数据组成的列表
        """
        return [i for i in self.collection.find()]

    def GetOneData(self):
        """
        通过随机数返回数据库内随机的一个元素
        :return:    返回一个数据库内元素
        """
        return self.collection.find_one(skip=randint(0, self.collection.count()))

    def UpdateTimes(self):
        """
        更新UnverfiedIP中的验证次数
        :return: 成功返回true失败返回false
        """
        self.collection.update_many({'_id': {'$exists': True}}, {'$inc': {'checktimes': 1}})


    def DeleteObsolete(self):
        """
        删除UnverifiedIP中的验证次数大于10次的ip
        :return: 成功返回true失败返回false
        """
        self.collection.delete_many({'checktimes': {'$gt': 5}})

    # c.create_index([('ip:port', pymongo.ASCENDING)], unique=True)  # 创建索引

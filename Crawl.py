from mongo.Mongopy import ConnectMongoProTable
from getproxyip import Proxyip
import CtrlFunc
import time


pip = Proxyip()
uv_ip_list = pip.getunVerifyIP()
start = time.clock()
database = ConnectMongoProTable('XXX.XXX.XXX.XXX', 27017, user={'username': 'user', 'password': 'pwd'})
CtrlFunc.CrawlToUvipDB(uv_ip_list, database.UnverifiedIP)
end = time.clock()
print('耗时', end-start)


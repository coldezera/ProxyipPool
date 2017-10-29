from mongo.Mongopy import ConnectMongoProTable
import CtrlFunc
import time


start = time.clock()
database = ConnectMongoProTable('XXX.XXX.XXX.XXX', 27017, user={'username': 'user', 'password': 'pwd'})
CtrlFunc.CheckVipToUvip(database.UnverifiedIP, database.verifiedIP)
end = time.clock()
print('耗时', end-start)

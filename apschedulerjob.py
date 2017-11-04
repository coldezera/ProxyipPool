from apscheduler.schedulers.background import BackgroundScheduler
from mongo.Mongopy import ConnectMongoProTable
import configparser
import CtrlFunc
from threading import Lock
import time


def GetDB():
    """
    读取配置文件链接数据库
    :return: 数据库对象
    """
    try:
        mongocfg = configparser.ConfigParser()
        file = mongocfg.read('E:/spider-progress/getproxyip/sched_conf.ini')
    except:
        Exception('configuration mongodb failed! plz check out sched_conf.ini!')
    if len(file) == 0:
        Exception('config file is empty!')
    sections = mongocfg.sections()
    return ConnectMongoProTable(mongocfg.get(sections[0], 'host'),
                                int(mongocfg.get(sections[0], 'port')),
                                user={
                                    'username': mongocfg.get(sections[0], 'user_name'),
                                    'password': mongocfg.get(sections[0], 'password')
                                })


class ProxyIPAPS:
    main_process_sche = None
    checker_sche = None

    def __init__(self):
        self.database = GetDB()
        job_defaults = {
            'coalesce': True,
            'max_instances': 1
        }
        self.main_process_sche = BackgroundScheduler(job_defaults=job_defaults)
        self.checker_process_sche = BackgroundScheduler(job_defaults=job_defaults)
        self.lock = Lock()

    def __main_process(self):

        @self.main_process_sche.scheduled_job('cron', minute='*/10')    # 爬取代理ip网页JOB
        def crawl_job():
            self.lock.acquire()
            CtrlFunc.CrawlToUvipDB(self.database.UnverifiedIP)
            self.lock.release()

        @self.main_process_sche.scheduled_job('cron', second='*/60')    # 验证UnverfiedIP JOB
        def checkuvip_job():
            self.lock.acquire()
            CtrlFunc.CheckUvipToVip(self.database.UnverifiedIP, self.database.verifiedIP)
            self.lock.release()

        @self.main_process_sche.scheduled_job('cron', second='*/20')    # 验证verfiedIP JOB
        def checkvip_job():
            self.lock.acquire()
            CtrlFunc.CheckVipToUvip(self.database.UnverifiedIP, self.database.verifiedIP)
            self.lock.release()

        pass

    def __check_process(self):
        @self.checker_process_sche.scheduled_job('cron', second='*/30') # 强制crawl JOB
        def force_crwal():
            self.lock.acquire()
            if CtrlFunc.CollectionCount(self.database.UnverifiedIP) < 0:
                CtrlFunc.CrawlToUvipDB(self.database.UnverifiedIP)
            self.lock.release()

        @self.checker_process_sche.scheduled_job('cron', second='*/10') # 强制验证UnverfiedIP JOB
        def force_checkuvip():
            self.lock.acquire()
            if CtrlFunc.CollectionCount(self.database.verifiedIP) < 10:
                CtrlFunc.CheckUvipToVip(self.database.UnverifiedIP, self.database.verifiedIP)
            self.lock.release()

    # def __test_process(self):
    #     @self.main_process_sche.scheduled_job('cron', second='*/2')
    #     def getdata_job():
    #         print(CtrlFunc.Get_OneIP(self.database.verifiedIP))

    def run(self):
        self.__main_process()
        self.__check_process()
        self.main_process_sche.start()
        self.checker_process_sche.start()
if __name__ == '__main__':
    a = ProxyIPAPS()
    a.run()
    while True:
        time.sleep(2)

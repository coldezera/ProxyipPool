# !/usr/bin/python
# -*- coding: utf8 -*-

import win32service
import win32serviceutil
import win32event
import os, time
from apschedulerjob import ProxyIPAPS
import traceback

"""
爬取代理ip网页ip10分钟爬取一次
UnverfiedIP中的ip没有之后强制crawl重新爬取一次，重置crawl倒计时
verfiedIP中的ip数量少于10之后强制验证UnverfiedIP一次，重置验证UnverfiedIP倒计时
验证UnverfiedIP45秒一次
验证verfiedIP每15秒一次
"""


class ProxyIPPool(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ProxyIPPoolService'
    _svc_display_name_ = 'ProxyIPPoolService'
    _svc_description_ = 'a task is crawl the proxy ip in the Internet and check the ip is useable'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        try:
            sched = ProxyIPAPS()
            sched.run()
        except Exception as e:
            print(repr(e))
            print(traceback.print_exc())
        while self.isAlive:
            time.sleep(2)
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False


if __name__ == '__main__':
    import sys
    import servicemanager

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(ProxyIPPool)
            servicemanager.Initialize('ProxyIPPool', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror

            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(ProxyIPPool)

import requests
from lxml import etree
import urllib
import json
import threading


ip181_page_header={
    'Host': 'www.ip181.com',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate'
}

xundaili_page_header={
    'Host': 'www.xdaili.cn',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.xdaili.cn/freeproxy',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest'
}


xicidaili_page_header = {
    'Host': 'www.xicidaili.com',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'If-None-Match': 'W/"09d7494b996df099c32f3c10d92b943e"'
}

yaoyaodaili_page_header = {
    'Host': 'www.httpsdaili.com',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate'
}

class Proxyip:
    """
    爬取代理ip网页的免费代理ip并验证ip的可用性
    """

    def __init__(self):
        """
        uv_ip_list: 未验证可用性ip列表
        """
        self.uv_ip_list = []

    def __parse_xiciip(self):     # 西刺代理(国内高匿和国内普通)42/200左右  √
        url_list = ['http://www.xicidaili.com/nn', 'http://www.xicidaili.com/nt/']
        for url in url_list:
            res = requests.get(url, headers=xicidaili_page_header)
            tree = etree.HTML(res.text)
            for ip_detail in tree.xpath('.//table[@id="ip_list"]//tr[@class]'):
                ip_addr = ''
                ip_addr = ':'.join(ip_detail.xpath('.//td/text()')[0:2])
                prot = ''.join(ip_detail.xpath('.//td[6]/text()'))
                self.uv_ip_list.append({
                    'ip:port': ip_addr,
                    'protocol': prot
                })

    def __parse_yaoyaoip(self):#瑶瑶代理 28/150左右  √(网站暂时无法访问)
        url_list = ['http://www.httpsdaili.com/free.asp?stype=1',
                    'http://www.httpsdaili.com/free.asp?stype=2',]
               # 'http://www.httpsdaili.com/free.asp?stype=1&page=2',
               # 'http://www.httpsdaili.com/free.asp?stype=2&page=2']
        for url in url_list:
            res = requests.get(url, headers=yaoyaodaili_page_header)
            tree = etree.HTML(res.text)
            for ip_detail in tree.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr'):
                ip_addr = ":".join(ip_detail.xpath('.//td/text()')[0:2])
                prot = ''.join(ip_detail.xpath('.//td[4]/text()'))
                self.uv_ip_list.append({
                    'ip:port': ip_addr,
                    'protocol': prot
                })

    def __parse_xundailiip(self):     # 讯代理 5/10的可用性 √
        url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
        res = requests.get(url, headers=xundaili_page_header)
        js = json.loads(res.text)
        ip_list = js['RESULT']['rows']
        for ip_detail in ip_list:
            self.uv_ip_list.append({
                            'ip:port': ip_detail['ip']+':'+ip_detail['port'],
                            'protocol': ip_detail['type']
                        })

    def __parse_ip181ip(self):    # ip181 25/100的可用性
        url = 'http://www.ip181.com/'
        res = requests.get(url, headers=ip181_page_header)
        tree = etree.HTML(res.text)
        for ip_detail in tree.xpath('//div[@class="col-md-12"]/table/tbody/tr[not(contains(@class,"active"))]'):
            self.uv_ip_list.append({
                'ip:port': ':'.join(ip_detail.xpath('.//td[1]/text() | .//td[2]/text()')),
                'protocol': ''.join(ip_detail.xpath('.//td[4]/text()'))
            })

    def getunVerifyIP(self):
        """
        通过爬取ip代理网页获得ip
        :return: 没有经过验证可用性的一组IP列表
        """
        self.__parse_xiciip()          # 西刺代理(国内高匿和国内普通)42/200左右
        # self.__parse_yaoyaoip()      # 瑶瑶代理 28/150左右  √(网站暂时无法访问)
        self.__parse_xundailiip()      # 讯代理 5/10的可用性 √
        self.__parse_ip181ip()         # ip181 25/100的可用性

        # print(self.uv_ip_list)
        print(len(self.uv_ip_list))
        return self.uv_ip_list

class CheckIP:

    def __init__(self, uip):
        """
        lock: 互斥锁
        useable_ip_list: 可用ip列表
        unusable_ip_list: 不可用ip列表
        uv_ip_list: 未验证可用性ip列表
        """
        self.lock = threading.Lock()
        self.useable_ip_list = []
        self.unusable_ip_list = []
        if not isinstance(uip, list):
            raise ValueError('传入的参数必须是list类型')
        self.uv_ip_list = uip

    def verifyIP(self):  # 验证IP的可用性
        url = 'http://www.whatismyip.com.tw/'
        # 共享变量是未验证的IP列表，通过锁来保护数据的互斥访问
        self.lock.acquire()
        ip = self.uv_ip_list.pop(0)
        self.lock.release()

        if ip['protocol'] == 'HTTP' or 'http' or 'HTTPS' or 'https' or 'HTTP/HTTPS' or 'HTTP,HTTPS':
            # print(ip['ip:port'], end='')
            proxy_ip = {'http': ip['ip:port']}
            proxy_support = urllib.request.ProxyHandler(proxy_ip)
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
            urllib.request.install_opener(opener)
            try:
                response = urllib.request.urlopen(url, timeout=5)
            except:
                self.lock.acquire()
                self.unusable_ip_list.append(ip)
                self.lock.release()
                print('连接失败')
            else:
                try:
                    text = response.read()
                    self.lock.acquire()
                    self.useable_ip_list.append(ip)
                    self.lock.release()
                except:
                    self.lock.acquire()
                    self.unusable_ip_list.append(ip)
                    self.lock.release()
                    print('html错误')
        pass

    def mulitverifyIP(self, get=None):

        '''
        多线程验证ip可用性
        :param get: 'useable' = 获取可用的ip列表 'unusable' = 获取不可用的ip列表
        :param ip_list: 尚未验证可用性的ip列表 不传入参数则为默认的ip列表
        :return: 返回get字符需要的ip列表
        '''
        if get == 'useable' or 'unusable' or 'useable_and_unusable':
            None
        else:
            raise ValueError('get参数传入错误值')

        threads = []
        for i in range(len(self.uv_ip_list)):
            threads.append(threading.Thread(target=self.verifyIP))
            threads[-1].start()
        for thread in threads:
            thread.join()
        if get is 'useable':
            return self.useable_ip_list
        elif get is 'useable_and_unusable':
            return self.useable_ip_list, self.unusable_ip_list
        else:
            return self.unusable_ip_list
        pass


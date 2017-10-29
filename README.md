# ProxyipPool
从几个有免费代理ip的网址爬取免费ip到本地mongodb数据库，定时验证ip可用性

***
## 下载之前
* **支持版本：Python3.6 MongoDB3.4**
* **需要安装的第三方库：pymongo, numpy, requests, lxml**
* **拥有一台云主机(可选，你也可以本地去跑，验证和收集ip我是放在我的云主机上去跑的，我本地只需要写一个API去获取云主机上数据库的数据即可)**

***

## 代码介绍
### getproxyip.py
    Proxyip类是爬取代理ip网址的免费ip的，类内的私有方法是从每个网站解析出ip地址和协议的。类内唯一一个非私有方法是整合所有私有方法获得的ip并返回出去的方法。
    （当然。如果你有更好的免费代理ip的网址，你也可以在这个类的加上新的解析网页的获得ip的私有方法，最后只需要在getunVerifyIP方法内加上你写的方法就可以了）
    
    CheckIP类是验证IP的可用性的类，采用多线程验证ip的可用性。

### mongo/Mongopy.py
    对pymongo的一些方法进行了简单的封装，使得在写代码中能够方便的去使用
    
### CtrlFunc.py
    此文件内的有个方法
    1、CrawlToUvipDB 将爬取的未经过验证的ip存进数据库
    2、CheckUvipToVip 从未验证的ip池内多线程验证可用的ip从库内删除并放入有效ip池，更新验证次数，对验证次数超过限制的ip删除
    3、CheckVipToUvip 验证有效ip池内的ip的可用性，将不可用的ip从库内删除并放入未验证ip池，放入之前重置这些ip的验证次数

### Crawl.py
    调用CrawlToUvipDB方法爬取ip存入未验证ip池
### CheckUvip.py
    调用CheckUvipToVip方法验证未验证ip池内的ip并将有用的入有效ip池
### CheckVip.py
    调用CheckVipToUvip方法验证有效ip池内的ip并将无用的ip入未验证ip池

    

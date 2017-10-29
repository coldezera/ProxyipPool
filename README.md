# ProxyipPool
从几个有免费代理ip的网址爬取免费ip到本地mongodb数据库，定时验证ip可用性

***
## 下载之前
* **支持版本：Python3.6 MongoDB3.4**
* **需要安装的第三方库：pymongo, numpy, requests, lxml**
* **拥有一台云主机(可选，你也可以本地去跑，验证和收集ip我是放在我的云主机上去跑的，我本地只需要写一个API去获取云主机上数据库的数据即可)**

***

##数据库方面
使用的Mongodb的数据库
数据存储格式：json

    {
        'ip:port':ip地址：端口
        'protocol':协议
        ‘checktimes’:检测次数
    }
    
### 创建数据库    
__貌似pymongo并没有创建数据库和collection的功能。只能对现有进行操作,所以创建数据库之类的操作，就在mongodb的shell那里创建了（**或许有什么方法能通过代码创建，也请知道的各位教我一下**）__

在mongodb中创建一个存放proxyip的数据库，创建两个collection，分别是UnverfiedIP和verfiedIP(名字随你喜欢取其他的也可以，但是代码里面的collection的名字也得记得改)

###创建数据库完毕后
先随便插入几条数据，然后通过代码手动创建一个索引
```python
collection.create_index([('ip:port', pymongo.ASCENDING)], unique=True)  # 创建索引
```
__两个collection都需要创建索引__

### Monggodb数据库授权设置
* 爬取ip验证ip的授权设置readWrite权限
* 获取可用ip的授权设置read权限
***

* #### 连接数据库方面可能遇到的问题

    * 连接本机数据库：连接本机的数据库授权其实可开可不开，BindIP就本地的。    
    * 连接远程数据库：建议绑定IP，开启授权设置，mongodb监听的端口记得查看是否处于打开状态
    * 连接云主机的数据库：建议绑定IP，开启授权设置，同时应该查看云主机的外部的配置，是否是外部的设置决定了端口能否被监听
    （我当初就是调试了2天的系统的设置，最后发现是云主机的配置没有允许这个端口。。）
    
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

    

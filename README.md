# ProxyipPool
从几个有免费代理ip的网址爬取免费ip到本地mongodb数据库，定时验证ip可用性。通过将程序写成windows服务的方式，让其在后台定时的维护代理ip池（程序和README正在完善中。。。2017.11.05）

***
## 下载之前
* **支持版本：Python3.6 MongoDB3.4**
* **需要安装的第三方库：pymongo, numpy, requests, lxml pywin32 apscheduler**
* **拥有一台云主机(可选，你也可以本地去跑，验证和收集ip我是放在我的云主机上去跑的，我本地只需要写一个API去获取云主机上数据库的数据即可)**

***

## 运行
1.

先修改sched_conf.ini文件内的配置参数，将数据库所在的ip和监听的端口，授权的用户名和密码填写进去（将apschedulerjob.py的第16行改为配置文件在你电脑上的**绝对路径**，一定要是绝对路径，不然启动服务时候会报错！）

2.

cmd 到你存放代码的根目录下安装服务，输入 
```bash
python ProxyipService.py install
```
如果想开机自启动服务的话就这么安装，输入
```bash
python ProxyipService.py --startup auto install 
```
先安装服务，如果有杀毒软件警告就忽略。安装完毕之后就是启动服务了
```bash
python ProxyipService.py start
```
如果启动服务成功则忽略以下步骤，如果报错1053则按照3.的方法解决

3.

⑴win+r打开运行，输入services.msc进入到服务的界面，在服务中找到自己安装的服务，名字是ProxyipService.py里面的类的\_svc\_name_属性。

⑵选中服务，**右键->属性**，点击**登录**选项卡，点击**此账户**再点击**浏览**，此时弹出一个新的对话框，点击**高级**，又弹出一个新的对话框

⑶点击**立即查找**会再搜索结果下面会出来结果，然后选中你电脑的管理员账户（通常都是结果里面的第一个吧），最后点击**确定**，回到了之前的对话框，再点击**确定**，退到了最开始的对话框

⑷最后在**密码**这一栏输入你的管理员账号的密码。**确认密码**那里再输入一次，最后点击**确定**。这样就能成功启动服务，不会报1053错误了。

__（我一开始也是遇到了1053的错误，但是百度许久未果，我一直猜测是权限的问题，这方法也是我自己瞎弄琢磨出来的，因为我的电脑开机是需要输入密码的，我猜测可能是这个原因，我也没有取消开机密码去测试一遍）__

4.
如果想停止服务就输入
```bash
python ProxyipService.py stop
```

5.

如果想删除服务话，先停止服务，再输入
```bash
python ProxyipService.py remove
```

***

## 数据库

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

### 创建数据库完毕后
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

## 流程图

![](https://github.com/coldezera/ProxyipPool/blob/master/image.jpg)


    爬取代理ip网页ip10分钟爬取一次
    UnverfiedIP中的ip没有之后强制crawl重新爬取一次，重置crawl倒计时
    verfiedIP中的ip数量少于10之后强制验证UnverfiedIP一次，重置验证UnverfiedIP倒计时
    验证UnverfiedIP45秒一次
    验证verfiedIP每15秒一次


## 代码介绍
### getproxyip.py
    Proxyip类是爬取代理ip网址的免费ip的，类内的私有方法是从每个网站解析出ip地址和协议的。类内唯一一个非私有方法是整合所有私有方法获得的ip并返回出去的方法。
    （当然。如果你有更好的免费代理ip的网址，你也可以在这个类的加上新的解析网页的获得ip的私有方法，最后只需要在getunVerifyIP方法内加上你写的方法就可以了）
    
    CheckIP类是验证IP的可用性的类，采用多线程验证ip的可用性。

### mongo/Mongopy.py
    对pymongo的一些方法进行了简单的封装，使得在写代码中能够方便的去使用
    （里面有设置了一个ip验证的次数如果超过5次都不可用的话，将会被自动删除。如果你想修改次数，请在第112行的数字出修改）
    
### CtrlFunc.py
    此文件内的有个方法
    1、CrawlToUvipDB 将爬取的未经过验证的ip存进数据库
    2、CheckUvipToVip 从未验证的ip池内多线程验证  可用的ip从库内删除并放入有效ip池，更新验证次数，对验证次数超过限制的ip删除
    3、CheckVipToUvip 验证有效ip池内的ip的可用性，将不可用的ip从库内删除并放入未验证ip池，放入之前重置这些ip的验证次数

### apschedulerjob.py
    使用apscheduler这个任务调度框架，预先设置好要执行的任务，还有任务执行的间隔时间。在这里可以修改爬取和验证的任务的时间间隔。
    我预设的时间间隔，在执行多几次之后，可用ip数据库最少的数量会在10多个左右，未验证的ip数据库最少的数量大概在50个左右，如果觉得这个数量不能满足要求，可以适当修改。
    但是免费ip毕竟可用率不高，可能修改之后效果也不太理想

### ProxyipService.py
    将代码的运行写入windows服务的脚本，调用apschedulerjob.py内的任务

## 最后
* **爬取的ip夹杂着高匿和普通，并没有对其进行分类，以后有时间估计会加上这个功能**
* **如果程序有什么问题或者BUG，也请告诉我，QQ：616775154 **

    

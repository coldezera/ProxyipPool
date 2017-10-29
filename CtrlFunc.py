from mongo.Mongopy import MymongoControl
from getproxyip import CheckIP


def CrawlToUvipDB(uviplist, collection):
    """
    处理爬虫获得的ip地址并存入到未验证ip的collection中
    :param uviplist:    爬虫获得的未验证ip表
    :param collection:  Mongodb的Collection对象
    :return: none
    """
    for ip in uviplist:
        ip['checktimes'] = 0
    collectionc = MymongoControl(collection)
    collectionc.InsertData(uviplist)


def CheckUvipToVip(uv_collection: MymongoControl, v_collection: MymongoControl):
    """
    拉取UnverifiedIP中的所有ip进行验证，然后把可用的ip增加到verifiedIP中去
    :param uv_collection:   UnverifiedIP的collection
    :param v_collection:    verifiedIP的collection
    :return: none
    """
    uv_collectionc = MymongoControl(uv_collection)
    v_collectionc = MymongoControl(v_collection)
    uvip = uv_collectionc.QueryAllData()
    ckip = CheckIP(uvip)
    useableip_list, unusableip_list = ckip.mulitverifyIP(get='useable_and_unusable')
    uv_collectionc.DeleteData(useableip_list)   # 删除可用
    uv_collectionc.UpdateTimes()    # 更新所有不可用的检测次数
    uv_collectionc.DeleteObsolete()     # 删除超过检测次数限制的IP
    v_collectionc.InsertData(useableip_list)


def CheckVipToUvip(uv_collection, v_collection):
    """
    拉取verifiedIP中的所有ip进行验证。把不可用的ip增加到UnverifiedIP中去
    :param uv_collection:   UnverifiedIP的collection
    :param v_collection:    verifiedIP的collection
    :return: none
    """
    uv_collectionc = MymongoControl(uv_collection)
    v_collectionc = MymongoControl(v_collection)
    vip = v_collectionc.QueryAllData()
    ckip = CheckIP(vip)
    unusableip_list = ckip.mulitverifyIP(get='unusable')
    v_collectionc.DeleteData(unusableip_list)   # 删除不可用
    for i in unusableip_list:       # 给不可用重新赋予为0的检测次数
        i['checktimes'] = 0
    uv_collectionc.InsertData(unusableip_list)

def Get_OneIP(v_collection):
    v_collectionc = MymongoControl(v_collection)
    return v_collectionc.GetOneData()['ip:port']





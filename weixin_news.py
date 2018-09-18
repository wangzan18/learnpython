#!/usr/bin/python
#coding:utf-8

import urllib2
import json
import sys
def getMsg(zabbix_msg):
    reload(sys)
    sys.setdefaultencoding('utf8')
    msg = ' '.join(zabbix_msg)
    msg = msg.split('#')
    mes="\n".join(msg)
    return "\n".join(msg)


if __name__ == '__main__':
    #微信公众号上应用的CropID和Secret
    CropID='wx8d46d36104988993'
    Secret='QCjzy2lH2ZB7MUG6uowChyChPsOQw96EB0X0QjofRRt0JePGezTVR4saIw3Ezznh'
 
    #获取access_token
    GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CropID,Secret)
    result=urllib2.urlopen(urllib2.Request(GURL)).read()
    dict_result = json.loads(result)
    dict_result.keys()
    Gtoken = dict_result['access_token']
    
    #生成通过post请求发送消息的url
    PURL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (Gtoken)
    
    AppID="4"                        #企业号中的应用id
#    UserID=2                       #部门成员id，zabbix中定义的微信接收者
    PartyID="2"                      #部门id，定义了范围，组内成员都可接收到消息

    #生成post请求信息
    post_data = {}
    textcard = {}
    textcard['description'] = getMsg(sys.argv[2:])
    textcard['title'] = getMsg(sys.argv[1:2])
    textcard['url'] = "www.wzlinux.com"
    textcard['btntxt'] = "请点击"

    #post_data['touser'] = UserID
    post_data['toparty'] = PartyID
    post_data['msgtype'] = 'textcard'
    post_data['agentid'] = AppID
    post_data['textcard'] = textcard
    #由于字典格式不能被识别，需要转换成json然后在作post请求
    #注：如果要发送的消息内容有中文的话，第三个参数一点要设为False
    json_post_data = json.dumps(post_data,False,False)
    #print(articles['title'])
    #通过urllib2.urlopen()方法发送post请求
    request_post = urllib2.urlopen(PURL, json_post_data)
    #read()方法查看请求的返回结果
    print request_post.read()

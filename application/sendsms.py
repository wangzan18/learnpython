#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import sys
client = AcsClient('LTAIfrefdkrHb0y', 'EytW2t5xdsfdfsEJ9mRfqf', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')
string = '10.0.2.6;Agent ping;18:02:32'
phone_number = '18817511223'
message = string.split(";")
dict1 = { }
dict1['host'] = message[0]
dict1['item'] = message[1]
dict1['time'] = message[2]
print(message)
request.add_query_param('RegionId', 'cn-hangzhou')
request.add_query_param('PhoneNumbers', phone_number)
request.add_query_param('SignName', '讯实监控报警')
request.add_query_param('TemplateCode', 'SMS_159772654')
request.add_query_param('TemplateParam', dict1)

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))

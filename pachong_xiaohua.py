# -*- coding:utf-8 -*-
import re
import requests

# 请求爬取的地址
respon = requests.get('http://www.xiaohuar.com/v/')

# 在响应的内容中，通过正则表达式匹配出url
urls = re.findall(r'class="items".*?href="(.*?)"',respon.text,re.S)
url = urls[5]
result = requests.get(url)
mp4_url = re.findall(r'id="media"')

from flask import Flask, render_template
import time
import requests
import re


app = Flask(__name__)


@app.route('/login')
def login():
    ctime = time.time() * 1000   # 模拟一个相同的时间戳
    base_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&' \
               'redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&' \
               'fun=new&lang=zh_CN&_={0}'
    url = base_url.format(ctime)   # 字符串拼接，生成新的url
    response = requests.get(url)   # 向新的url发送get请求
    xcode_list = re.findall('window.QRLogin.uuid = "(.*)";', response.text)  # 获取二维码的参数
    # req.session['xcode'] = xcode_list[0]
    return render_template('login.html', xcode=xcode_list[0])


def check_login():
    pass


if __name__ == '__main__':
    app.run(debug=True)

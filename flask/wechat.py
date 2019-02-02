
from flask import Flask, render_template, request, session, jsonify
import time
import requests
import re
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'wangzan18'


def xml_parser(text):
    """
    格式化xml数据，修改成我们需要的格式
    :param text:
    :return:
    """
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    获取登录的二维码
    :return:
    """
    if request.method == 'GET':
        ctime = time.time() * 1000   # 模拟一个相同的时间戳
        base_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&' \
               'redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&' \
               'fun=new&lang=zh_CN&_={0}'
        url = base_url.format(ctime)   # 字符串拼接，生成新的url
        response = requests.get(url)   # 向新的url发送get请求
        qcode = re.findall('uuid = "(.*)";', response.text)[0]  # 获取二维码的参数
        session['qcode'] = qcode
        return render_template('login.html', qcode=qcode)
    else:
        pass


@app.route('/check_login')
def check_login():
    """
    检查用户是否扫码登录
    :return:
    """
    response = {'code': 408}  # 默认用户没有扫码
    qcode = session.get('qcode')  # 获取用户前面获取的 uuid，用于放到下面的 url 里面
    ctime = time.time() * 1000
    check_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-1437802572&_={1}".format(qcode, ctime)
    ret = requests.get(check_url)  # 扫码返回值
    if 'code=201' in ret.text:
        # 扫码成功
        src = re.findall("userAvatar = '(.*)';", ret.text)[0]  # 获取扫码用户头像
        response['code'] = 201  # 获取扫码的返回值，放到字典response
        response['src'] = src  # 获取用户头像数据，放到字典response
    elif 'code=200' in ret.text:
        # 确认登录
        redirect_uri = re.findall('redirect_uri="(.*)";', ret.text)[0]   # 获取跳转的url

        # 向redirect_uri地址发送请求，获取凭证相关信息
        redirect_uri = redirect_uri + "&fun=new&version=v2&lang=zh_CN"
        ticket_ret = requests.get(redirect_uri)  # 获取xml参数
        ticket_dict = xml_parser(ticket_ret.text)  # 解析参数变成我们需要的格式
        session['ticket_dict'] = ticket_dict   # 或许我们初始化需要的ticket
        response['code'] = 200
    return jsonify(response)


@app.route('/index')
def index():
    ticket_dict = session.get('ticket_dict')  # 获取初始化需要的ticket
    if ticket_dict:
        init_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1438401779&lang=zh_CN&pass_ticket={0}".format(
            ticket_dict.get('pass_ticket'))   # 调整好初始化的url
        data_dict = {
            "BaseRequest": {
                   "Sid": ticket_dict.get('wxsid'),
                   "Uin": ticket_dict.get('wxuin'),
                   "Skey": ticket_dict.get('skey'),
               }
        }    # post需要的参数
        init_ret = requests.post(url=init_url, json=data_dict)  # 微信登录初始化
        init_ret.encoding = 'utf-8'
        user_dict = init_ret.json()  # 储存返回的json数据
        # print(user_dict['ContactList'])
        return render_template('index.html', user_dict=user_dict)  # 把返回的数据传给index.html


@app.route('/contact_all/')
def contact_all():
    ticket_dict = session.get('ticket_dict')  # 获取初始化需要的ticket
    skey = ticket_dict.get('skey')
    pass_ticket = ticket_dict.get('pass_ticket')
    base_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket={0}&r={" \
               "1}&seq=0&skey={2}".format(pass_ticket, time.time() * 1000, skey)
    r1 = requests.get(base_url, cookies=ticket_dict)
    contact_dict = json.loads(r1.content)
    # for item in contact_dict["MemberList"]:
    #     print(item)
    return render_template('contact_all.html', contact_dict=contact_dict)


if __name__ == '__main__':
    app.run(debug=True)

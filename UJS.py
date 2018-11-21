import requests
from PIL import Image
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote,quote
import os

def Login():
    # 登录验证部分
    url = "http://my.ujs.edu.cn//userPasswordValidate.portal"
    headers = {
        "referer": "http://my.ujs.edu.cn/index.portal",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    session = requests.session()
    response1 = session.get(url=url, headers=headers)
    # html1 = response1.text
    qrcode_url = "http://my.ujs.edu.cn/captchaGenerate.portal?s=0.11031588373022694"
    response2 = session.get(url=qrcode_url, headers=headers)
    with open("qrcode.jpg", "wb") as qrcode:
        qrcode.write(response2.content)
    img = Image.open("qrcode.jpg")
    user = input("学号:")
    password = input("密码:")
    # name=input("姓名:")
    data = {
        "Login.Token1": user,
        "Login.Token2": password,
        "goto": "http://my.ujs.edu.cn/loginSuccess.portal",
        "gotoOnFail": "http://my.ujs.edu.cn/loginFailure.portal"
    }
    data['captchaField'] = input('输入验证码:')

    response3 = session.post(url=url, data=data, headers=headers)
    if "handleLoginSuccessed();" in response3.text:
        #print("\033[1;32m登录成功!\033[0m")
        return 1,session,user
    else:
        #print("\033[0;31m登录失败!\033[0m")
        return 0,session,user
def Login_in(session):
    # 进入index.portal
    headers_test = {
        "referer": "http://my.ujs.edu.cn/index.portal",
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Host": "xk1.ujs.edu.cn",
        "Upgrade-Insecure-Requests": "1"
    }
    headers_name = {
        "referer": "http://my.ujs.edu.cn/login.portal",
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    # 获取用户名字，来做二次验证
    response_name = session.get(url="http://my.ujs.edu.cn/index.portal", headers=headers_name)
    html = etree.HTML(response_name.text)
    result = html.xpath("//div[@id='topMenu']/div")
    name = result[2].text.partition(",")[0]
    # Cookie={
    #     "UqZBpD3n3iXPAw1X9ACormqiXu4A8INFZA@@":"v1y3PtQwSDAs7",
    #     "amlbcookie":"01",
    #     "iPlanetDirectoryPro":"AQIC5wM2LY4Sfcw6jbXFs%2FkCe8S1n6%2BxGEO6Fidgbe8S9EI%3D%40AAJTSQACMDE%3D%23"
    # }
    response_test = session.get(url="http://xk1.ujs.edu.cn/default_zzjk.aspx", headers=headers_test)
    # 获得选课系统的服务器返回的数字
    url1 = response_test.url.rpartition("/")[0]
    return url1,name

def curriculum(session, user,url1,name):
    url2 = url1 + "/xskbcx.aspx?xh=" + user + "&xm=" + quote(name, encoding="GBK") + "&gnmkdm=N121602"
    headers2 = {
        "referer": url1 + "/xs_main_zzjk1.aspx?xh=3150601024&type=1",
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    data2 = {
        "xh": user,
        "xm": quote(name, encoding="GBK"),
        "gnmkdm": "N121602"
    }
    response4 = session.post(url2, headers=headers2, data=data2)
    # 通过Beautiful匹配课表
    result = BeautifulSoup(response4.text, "html.parser")
    curriculum = result.find(name="table", class_="blacktab")
    # print(curriculum)dag
    today = datetime.today()
    today_date = datetime.date(today)
    name = "课程表-"+name+"-"
    if curriculum is not None:
        print("课程表爬取成功")
        file_name = os.getcwd() + "\\" + name + str(today_date) + ".html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(
                "<!DOCTYPE html><html><head><title></title><style type='text/css'>.blacktab th,.blacktab td{border: 1px solid #000;color:#000;}.blacktab{border-collapse:collapse;}</style></head><body>" + str(curriculum) + "</body></html>")
        print("File saved at " + os.getcwd() + "\\" + name + str(today_date) + '.html')
    else:
        print("课程表爬取失败")
    return url2
def grade(session,user,url1,name):
    url3=url1+"/xscjcx.aspx?xh=" + user + "&xm=" + quote(name, encoding="GBK") + "&gnmkdm=N121615"
    headers={
        "referer":url1 + "/xskbcx.aspx?xh=" + user + "&xm=" + quote(name, encoding="GBK") + "&gnmkdm=N121615",
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    data={
        "xh": user,
        "xm": quote(name, encoding="GBK"),
        "gnmkdm": "N121615",
        "btn_zcj":"%C0%FA%C4%EA%B3%C9%BC%A8"
    }
    response5=session.post(url3,headers=headers,data=data)
    html = etree.HTML(response5.text)
    result = html.xpath("//*[@id='Form1']/input[3]/@value")[0]
    data_with_value={
        "xh": user,
        "xm": quote(name, encoding="GBK"),
        "gnmkdm": "N121615",
        "btn_zcj": "%C0%FA%C4%EA%B3%C9%BC%A8",
        "__VIEWSTATE":result
    }
    response6=session.post(url3,headers=headers,data=data_with_value)
    # print(response6.text)
    grade_result = BeautifulSoup(response6.text, "html.parser")
    grade = grade_result.find(name="table", class_="datelist")
    # print(grade.text)
    name = "总成绩表-" + name + "-"
    if grade is not None:
        print("成绩爬取成功")
        file_name = os.getcwd() + "\\" + name  + ".html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(
                "<!DOCTYPE html><html><head><title></title><style type='text/css'>.datelist{border: 1px solid #ccc;border-collapse: collapse;width: 100%;margin: 2px auto;}.datelist tbody td, .datelist tbody th{border: 1px solid #000;color:#000;}.datelist tr.alt{background: #F8F7F7;}</style></head><body>" + str(grade) + "</body></html>")
        print("File saved at " + os.getcwd() + "\\" + name  + '.html')
    else:
        print("成绩爬取失败")
if __name__ == '__main__':
    Login_num,session,user=Login()
    if Login_num==1:
        print("\033[1;32m登录成功!\033[0m")
    elif Login_num==0:
        print("\033[0;31m登录失败!\033[0m")
    url1,name=Login_in(session)
    curriculum(session,user,url1,name)
    grade(session,user,url1,name)

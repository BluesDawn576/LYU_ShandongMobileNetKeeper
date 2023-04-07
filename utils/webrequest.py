import os

import requests
import json

from utils import console
from utils import page

redirect_url = "http://1.1.1.1"
ip = "223.99.141.139:10088"
login_url = "http://{}/web/connect".format(ip)
# status_url = "http://{}/web/status".format(ip)


def login(user, password, mac):
    try:
        print("------登录------")
        console.log("尝试使你登录")
        console.log("获取重定向连接...")
        res = requests.get(redirect_url, allow_redirects=False)
        if not res.headers.get('Location'):
            console.alert(
                "重定向无效，不在特定的网络环境下\n可能的原因：\n1. 已登录校园网，无需再次登录\n2. 路由器配置不正确，无法连接至互联网\n3. 非 NetKeeper 校园网，无需使用此程序\n",
                "错误")
            return
        location = res.headers['Location']
        if (len(location) > 17) and (mac is not None):
            location = location[0:-17] + mac
        console.log("重定向到{}".format(location))

        data = {
            "web-auth-user": user,
            "web-auth-password": password,
            "remember-credentials": "false",
            "redirect-url": location
        }
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": ip,
            "Origin": "http://{}".format(ip),
            "Referer": location,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
            "X-Requested-With": "XMLHttpRequest"
        }

        console.log("启动登录进程")
        res = requests.post(login_url, data, headers=header)
        console.log("回应代码: {}".format(res.status_code))

        if res.status_code == 200:
            console.alert("登录成功", "提示")
            page.redirect_window()
        else:
            data = json.loads(res.text)
            err_code = data["error"]
            if err_code == 142:
                console.alert(
                    "重定向无效，不在特定的网络环境下\n可能的原因：\n1. 已登录校园网，无需再次登录\n2. 路由器配置不正确，无法连接至互联网\n3. 非 NetKeeper 校园网，无需使用此程序\n" +
                    data["error_description"], "错误")
            elif err_code == 81:
                if "The subscriber is deregistered or the password is incorrect." in data["error_description"]:
                    console.alert("登录失败，账号或密码不正确\n" + data["error_description"], "错误")
                else:
                    console.alert("登录失败\n" + data["error_description"], "错误")
            else:
                console.alert(data["error_description"], "错误")
            print(data["error_description"])
            page.close_console_panel()
    except requests.exceptions.ConnectTimeout as err:
        console.alert("连接超时\n" + str(err), "异常")
    except requests.exceptions.ConnectionError as err:
        console.alert("连接错误\n可能的原因：\n1. 未连接网络\n2. 路由器配置不正确，无法连接至互联网\n" + str(err), "异常")
    except BaseException as err:
        console.alert("执行代码时出错：\n{}\nline {}: {}".format(
            err.__traceback__.tb_frame.f_globals["__file__"],
            err.__traceback__.tb_lineno,
            err), "异常")
    finally:
        page.close_console_panel()

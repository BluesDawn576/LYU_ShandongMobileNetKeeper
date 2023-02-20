import requests
import os
import json
import time
import configparser
import win32api
import win32con
import random

class LoginManager:
    '''
    登录处理
    '''
    @staticmethod
    def readInfo(user = None, password = None, mac = None):
        print("--------登录--------")
        if user != None and password != None:
            print("登录账号: {}".format(user))
            print("登录密码: {}".format(password))
            print("请稍等......")
            LoginManager.connectWeb(user,password,mac)
        else:
            fileName = "accinfo.ini"
            conf = configparser.ConfigParser()
            conf.read(fileName)
            if os.path.exists(fileName):
                user = conf.get('config', 'user')
                password = conf.get('config', 'password')
                if user == "" or password == "":
                    win32api.MessageBox(0, "请填写账号密码(\n例：\n[config]\nuser = 11451419198\npassword = 123456", "错误",win32con.MB_ICONERROR)
                    File.OpenFile(fileName)
                    LoginManager.readInfo()
                else:
                    print("登录账号: {}".format(user))
                    print("登录密码: {}".format(password))
                    print("请稍等......")
                    LoginManager.connectWeb(user,password,mac)
            else:
                print("配置文件错误或不存在")
                print("首次启动需要提供上网账号与密码")
                print("在运行目录 \"{}\" 生成 accinfo.ini".format(os.getcwd()))
                conf.add_section('config')
                conf.set('config', 'user', '')
                conf.set('config', 'password', '')
                with open(fileName, 'w') as fw:
                    conf.write(fw)
                print("请在accinfo.ini中填写上网账号(user)与密码(password)，保存并关闭")
                win32api.MessageBox(0, "首次启动需要提供上网账号与密码，请在accinfo.ini中填写上网账号(user)与密码(password)，保存并关闭\n例：\n[config]\nuser = 11451419198\npassword = 123456", "提示",win32con.MB_ICONASTERISK)
                File.OpenFile(fileName)
                LoginManager.readInfo()

    @staticmethod
    def connectWeb(user,password,mac):
        url = "http://1.1.1.1"
        res = requests.get(url,allow_redirects=False)
        location = res.headers["Location"]
        if mac != None:
            location = location[0:-17] + mac
        print("重定向到{}".format(location))
        LoginManager.login(user,password,location)

    @staticmethod
    def login(user,password,location):
        ip = "223.99.141.139:10088" #登录页面固定ip，不能保证全部地区都适用
        url = "http://{}/web/connect".format(ip)

        #伪造请求头与请求体
        data = {
            "web-auth-user": user,
            "web-auth-password": password,
            "remember-credentials": "false",
            "redirect-url": location
        }
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "219",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": ip,
            "Origin": "http://{}".format(ip),
            "Referer": location,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = requests.post(url,data,headers=header)
        print(res.text)
        print("回应代码: {}".format(res.status_code))

        if res.status_code == 200:
            url = "http://{}/web/status".format(ip)
            res_status = json.loads(res.text)
            created_at, started_at = res_status["created_at"], res_status["session"]["started_at"]
            if abs(created_at - started_at) >= 5:
                err_code = -233
                print("--------ERROR--------\n表单异常\n请求时间：{}\n开始时间：{}\n".format(
                    time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(created_at)),
                    time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(started_at))
                ))
                print("\n尝试通过伪造Mac地址登录")
                global COUNT
                COUNT += 1
                random_mac = RandomMAC()
                print("第{}次尝试：{}".format(COUNT, random_mac))
                LoginManager.readInfo(user, password, random_mac)
            else:
                #MsgBox.Load(200, "提示", "登录成功", win32con.MB_ICONASTERISK)
                print("登录成功")
                time.sleep(1)
                File.OpenFile("Update.exe") #调用更新程序检查有无更新
        else:
            data = json.loads(res.text)
            err_code = data["error"]
            if err_code == 142:
                MsgBox.Load(err_code, "错误", data["error_description"] + "\n重定向无效，不在特定的网络环境下", win32con.MB_ICONERROR)
                File.OpenFile("Update.exe")
            elif err_code == 81:
                if "The subscriber is deregistered or the password is incorrect." in data["error_description"]:
                    MsgBox.Load(err_code, "错误", data["error_description"] + "\n登录失败，账号或密码不正确", win32con.MB_ICONERROR)
                else:
                    MsgBox.Load(err_code, "错误", data["error_description"] + "\n登录失败，该账号可能被其他设备占用", win32con.MB_ICONERROR)
                MsgBox.Load(err_code, "提示", "请手动输入账号密码", win32con.MB_ICONERROR)
                print("--------重新输入--------")
                user = input("请输入用户名：")
                password = input("请输入密码：")
                LoginManager.readInfo(user, password)
            else:
                MsgBox.Load(err_code, "错误", data["error_description"], win32con.MB_ICONERROR)

class File:
    @staticmethod
    def OpenFile(name):
        os.system('"{}\\{}"'.format(os.getcwd(), name))

class MsgBox:
    @staticmethod
    def Load(err_code, err, string, type):
        print(string)
        win32api.MessageBox(0, string, "{} {}".format(err, err_code), type)

# 伪造mac地址
def RandomMAC():
    mac = [ 0x52, 0x54, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return '-'.join(map(lambda x: "%02x" % x, mac))

if __name__ == '__main__':
    print("NetKeeper山东移动高校宽带一键登录 v1.4.0")

    COUNT = 0

    try:
        LoginManager.readInfo()
    except BaseException as err:
        print("--------ERROR--------")
        if "Failed to establish a new connection" in str(err):
            MsgBox.Load("", "异常", "没有连接到网络", win32con.MB_ICONERROR)
        else:
            MsgBox.Load("", "异常", "执行指令时出错：\n{}\nline {}: {}".format(
        err.__traceback__.tb_frame.f_globals["__file__"],
        err.__traceback__.tb_lineno,
        err), win32con.MB_ICONERROR)
        os.system("pause")

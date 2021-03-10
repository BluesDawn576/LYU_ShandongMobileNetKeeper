import requests
import os
import json
import configparser
import win32api
import win32con

class LoginManager:
    '''
    登录处理
    '''
    @staticmethod
    def readInfo():
        fileName = "accinfo.ini" #在软件根目录生成一个ini文件
        conf = configparser.ConfigParser()
        conf.read(fileName)
        if os.path.exists(fileName):
            user = conf.get('config', 'user')
            password = conf.get('config', 'password')
            if user == "" or password == "":
                win32api.MessageBox(0, "你想拿空气登录吗(\n例：\n[config]\nuser = 11451419198\npassword = 123456", "错误",win32con.MB_ICONERROR)
                File.OpenFile(fileName)
                LoginManager.readInfo()
            else:
                print("登录账号: {}".format(user))
                print("登录密码: {}".format(password))
                print("请稍等......")
                LoginManager.connectWeb(user,password)
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
    def connectWeb(user,password):
        url = "http://1.1.1.1"
        res = requests.get(url,allow_redirects=False)
        location = res.headers["Location"]
        print("重定向到{}".format(location))
        LoginManager.login(user,password,location)

    @staticmethod
    def login(user,password,location):
        ip = "223.99.141.139:9090" #登录页面固定ip，不能保证全部地区都适用
        url = "http://{}/web/connect".format(ip)

        #伪造请求头与请求体
        data = {
            "web-auth-user": user,
            "web-auth-password": password,
            "redirect-url": location
        }
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "219",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "BIGipServersc-ltm-xywpt-portal3-pool=135926188.33315.0000",
            "Host": ip,
            "Origin": "http://{}".format(ip),
            "Referer": location,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = requests.post(url,data,headers=header)
        print("回应代码: {}".format(res.status_code))

        if res.status_code == 200:
            print("登录成功")
            win32api.MessageBox(0, "登录成功", "提示",win32con.MB_ICONASTERISK)
            File.OpenFile("Update.exe") #调用更新程序检查有无更新
        else:
            data = json.loads(res.text)
            err_code = data["error"]
            print("错误代码: {}\n{}".format(err_code,data["error_description"]))
            if err_code == 142:
                print("不在特定的网络环境下")
            else:
                print("登录失败，请检查账号密码是否正确/是否被其它设备占用")
            win32api.MessageBox(0, "登录失败，请关闭重试，报错内容请查看控制台", "错误",win32con.MB_ICONERROR)
            os.system("pause")

class File:
    @staticmethod
    def OpenFile(name):
        os.system('"{}\\{}"'.format(os.getcwd(),name))

if __name__ == '__main__':
    try:
        print("NetKeeper山东移动高校宽带一键登录 v1.1.0.4")
        print("https://github.com/BluesDawn576/LYU_ShandongMobileNetKeeper")
        print("---------------------------")
        LoginManager.readInfo()
    except BaseException as err:
        print("--------异常--------")
        print(str(err))
        win32api.MessageBox(0, "程序异常，报错内容请查看控制台", "异常",win32con.MB_ICONERROR)
        os.system("pause")
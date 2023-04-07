import sys, io

sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

import eel
import platform
import win32api, win32con

from utils import account
from utils import webrequest
from utils import mac

print("NetKeeper山东移动高校宽带一键登录")
print("启动中...")

eel.init('src')


@eel.expose
def get_accinfo():
    return account.get_account_info()


@eel.expose
def set_accinfo(user, password):
    account.set_account_info(user, password)


@eel.expose
def login(user, password):
    webrequest.login(user, password, mac.random_mac())


try:
    eel.start('index.html', size=(800, 600), port=0)
except EnvironmentError:
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start('hello.html', mode='edge', size=(800, 600), port=0)
    else:
        win32api.MessageBox(0, "系统不是 Windows 10 或更高版本", "错误", win32con.MB_ICONERROR)
        raise EnvironmentError('Error: System is not Windows 10 or above')

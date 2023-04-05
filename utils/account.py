import os
import configparser

conf = configparser.ConfigParser()
file_name = "accinfo.ini"


def get_account_info():
    if os.path.exists(file_name):
        conf.read(file_name)
        user = conf.get('config', 'user')
        password = conf.get('config', 'password')
        return [user, password]
    return None


def set_account_info(user, password):
    if os.path.exists(file_name):
        conf.read(file_name)
        current_user = conf.get('config', 'user')
        current_password = conf.get('config', 'password')
        if current_user == user and current_password == password:
            return
    if not conf.has_section('config'):
        conf.add_section('config')
    conf.set('config', 'user', user)
    conf.set('config', 'password', password)
    with open(file_name, 'w') as fw:
        conf.write(fw)

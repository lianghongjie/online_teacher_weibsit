# -*- coding: utf-8 -*-


# class A(object):
#     name_2 = 'test_2'
#
#     def __init__(self):
#         self.name = 'test'
#
# a = A()
# b = A()
# a.name_2 = 'tt'
# A.name_2 = 'hh'
# print a.name_2, b.name_2, A.name_2
# A.name = 'ff'
# print a.name, b.name, A.name, A().name


import requests
import re

headers = {
    'Rerferer': '',
    'User-Agent': '',
    'HOST': '',
}

# <input name="atl_token" type="hidden" value="B62M-0W0A-4LU5-W45P|f31e3e81d45bf11d23ff50f621c24c335be42620|lin">
# .*\<input name="atl_token" .*value="(?P<atl_token>.*)".*\>.*
# os_username:lianghj
# os_password:#Ekrhy8X
# os_destination:
# user_role:
# atl_token:
# login:Log In
# < input
#
# name = "atl_token"
#
# type = "hidden"
#
# / > .*value="(?P<atl_token>.*)".*\>.*>  .*\<input\s*name\s*=\s*"\s*atl_token\s*".*\>.*


def get_atl_token():
    response = requests.post(url='https://ticket.base-fx.com/login.jsp')
    # print response.text
    atl_match = re.match('.*(\<\s*input\s*name\s*=\s*"\s*atl_token\s*"\s*.*\>).*', response.text)
    print atl_match.group()

def login():
    post_data = {
        'os_username': 'lianghj',
        'os_password': '#Ekrhy8X',
        'os_destination': '',
        'user_role': '',
        'atl_token': ''
    }

    response = requests.post(url='http://confluence.base-fx.com:8090/login.action', data=post_data)
    print response


def is_login():
    response = requests.get(url='https://ticket.base-fx.com/browse/PLE-934', allow_redirects=False)
    if response.status_code != 200:
        print 'status_code:', response.status_code, '未登陆!'
        return False
    else:
        print 'status_code:', response.status_code, '登陆成功!'
        return True

# get_atl_token()
login()
is_login()
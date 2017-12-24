# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random


from users.models import EmailCode
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM


def send_email_code(email, type_='register'):
    email_code = EmailCode()
    code = generate_email_code(16)
    email_code.code = code
    email_code.email = email
    email_code.send_type = type_
    email_code.save()

    email_title = ''
    email_body = ''
    if type_ == 'register':
        email_title = '慕课在线激活'
        email_body = '欢迎使用慕课在线网,激活请点击下面链接\nhttp://127.0.0.1:8000/active/{0}'.format(code)

    send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email, ])
    if send_status:
        pass

    elif type_ == 'forget':
        email_title = '慕课在线找回密码'
        email_body = '欢迎使用慕课在线网找回密码请点击下面链接\nhttp://127.0.0.1:8000/forget_password/{0}'.format(code)

    send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email, ])
    if send_status:
        pass


def generate_email_code(length=16):
    lower_str = map(chr, range(97, 123))
    upper_str = [i.upper() for i in lower_str]
    number = map(str, range(9))
    upper_str.extend(number)
    lower_str.extend(upper_str)
    return ''.join(random.sample(lower_str, length))



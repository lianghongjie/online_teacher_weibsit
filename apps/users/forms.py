# -*- coding: utf-8 -*-

# forms 的作用是对数据进行预处理， 防止post http请求时出现大量的逻辑，它是一种预处理的功能
from __future__ import unicode_literals

from django import forms
from captcha.fields import CaptchaField


class LoginForms(forms.Form):
    # 这里的username 和password 必须的login.html中的<input username/>字段一致才可以进行检测
    username = forms.CharField(required=True)  # required的作用是字段不为空，为空会以表单的形式报错（必填字段）
    password = forms.CharField(required=True, min_length=5)  # 如果最小长度小于5的话为提示错误（不会进入到数据库中查询）


class RegisterForms(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


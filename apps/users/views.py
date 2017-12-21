# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from forms import LoginForms, RegisterForms
from .models import UserWrapper, EmailCode
from utils.send_email import send_email_code


class UserLoginView(View):
    def post(self, request):
        login_forms = LoginForms(request.POST)  # request.POST 是从login.html传进来的,login.html中的<input username/>字段
        if login_forms.is_valid():  # 检测forms是否通过
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user_authenticate = authenticate(username=user_name, password=pass_word) # authenticate能够查询到数据中的信息
            if user_authenticate:
                if user_authenticate.is_active():
                    login(request, user_authenticate)
                    return render(request, template_name='index.html', context={})
                else:
                    return render(request, template_name='login.html', context={'message': '用户未激活'})
            else:
                return render(request, template_name='login.html', context={'message': '用户或密码错误'})
        else:
            return render(request, template_name='login.html', context={'login_forms': login_forms})

    def get(self, request):
        return render(request=request, template_name='login.html', context={})


class ActiveUserView(View):
    def get(self, request, register_code):
        email_code_objects = EmailCode().objects.filter(email_code=register_code)
        if email_code_objects:
            for email_code_object in email_code_objects:
                email = email_code_object.email
                user_wrapper = UserWrapper().objects.get(email=email)
                user_wrapper.is_active = True
                user_wrapper.save()
            return render(request, template_name='login.html')
        else:
            return render(request, template_name='register.html', context={})

    def post(self, request):
        pass


class RegisterView(View):
    def get(self, request):
        register_forms = RegisterForms(request.POST)
        return render(request, template_name='register.html', context={'register_forms': register_forms})

    def post(self, request):
        register_forms = RegisterForms(request.POST)
        if register_forms.is_valid():
            email = request.POST.get('email', '')
            if UserWrapper.objects.get(email=email):
                return render(request, template_name='register.html', context={'register_forms': register_forms,
                                                                               'message': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_wrapper = UserWrapper()
            user_wrapper.email = email
            user_wrapper.is_active = False
            user_wrapper.password = pass_word
            user_wrapper.save()

            send_email_code(email, 'register')
            return render(request, template_name='login.html', context={})
        else:
            return render(request, template_name='register.html', context={'register_forms': register_forms})

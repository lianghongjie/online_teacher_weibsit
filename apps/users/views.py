# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from forms import LoginForms, RegisterForms, ForgetForms, ModifyPassword
from .models import UserWrapper, EmailCode
from utils.send_email import send_email_code
from django.contrib.auth.hashers import make_password


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
        email_code_objects = EmailCode.objects.filter(email_code=register_code)
        if email_code_objects:
            for email_code_object in email_code_objects:
                email = email_code_object.email
                user_wrapper = UserWrapper.objects.get(email=email)
                user_wrapper.is_active = True
                user_wrapper.save()
            return render(request, template_name='login.html')
        else:
            return render(request, template_name='active_fail.html', context={})

    def post(self, request):
        modify_form = ModifyPassword(request.POST)
        if modify_form.is_valid():
            html_password1 = request.POST.get('password', '')
            html_password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if html_password1 == html_password2:
                user_wrapper = UserWrapper.objects.get(email=email)
                assert user_wrapper
                user_wrapper.password = make_password(html_password2)
                user_wrapper.save()
                return render(request, template_name='login.html')
            else:
                return render(request, template_name='password_reset.html', content_type=
                {'email': email, 'message': '密码输入不一致，请重新输入'})
        else:
            return render(request, template_name='password_reset.html', content_type={'modify_form': modify_form})


class ResetPassword(View):
    def get(self, request, reset_code):
        # email_code = EmailCode.objects.get(code=reset_code)  # get如果查找code不存在就会返回异常
        email_code_object = EmailCode.objects.filter(code=reset_code)  # filter如果查查寻不到code就会返回[] return list
        if email_code_object and email_code_object.__len__() == 1:
            email = email_code_object[0].email
            user_wrapper = UserWrapper.objects.get(email=email)
            return render(request, 'password_reset.html', content_type={'email': email})
        elif email_code_object and email_code_object.__len__() > 1:
            return render(request, 'forgetpwd.html', content_type={'message': '找回密码验证码错误，并进行从新发送'})


class SetPasswordView(View):
    def get(self, request):
        pass

    def post(self, request):
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')


class ForgetPassword(View):
    def get(self, request):
        forget_forms = ForgetForms(request.POST)
        return render(request, template_name='forgetpwd.html', context={'forget_forms': forget_forms})

    def post(self, request):
        forget_forms = ForgetForms(request.POST)
        email = request.POST.get('email', '')
        if forget_forms.is_valid():
            send_email_code(email, 'forget')
            return render(request, template_name='send_success.html')
        else:
            return render(request, template_name='forgetpwd.html', context={'email': email, 'forget_forms': forget_forms})


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

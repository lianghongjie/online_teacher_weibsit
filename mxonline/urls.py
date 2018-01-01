# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from users.views import UserLoginView, RegisterView, ActiveUserView, ResetPassword, SetPasswordView, ForgetPassword
from organization.views import OrganizationListView
from django.views.static import serve
from settings import MEDIA_ROOT
import captcha


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<register_code>.*)/$', ActiveUserView.as_view(), name='register_code'),
    url(r'forget/$', ForgetPassword.as_view(), name='forget_password'),
    url(r'^reset/(?P<reset_code>[0-9]+)', ResetPassword.as_view(), name='reset_code'),
    url(r'^reset_password/$', SetPasswordView.as_view(), name='reset_password'),

    # 课程机构列表
    url(r'^organization_list/$', OrganizationListView.as_view(), name='organization_list'),

    # 配置media文件路径
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT})  # 固定字段document
]

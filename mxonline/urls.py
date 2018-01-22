# -*- coding: utf-8 -*-

from django.conf.urls import url, include
import xadmin
from django.contrib import admin
from django.views.generic import TemplateView
from users.views import UserLoginView, RegisterView, ActiveUserView, ResetPassword, SetPasswordView, ForgetPassword, IndexView
from organization.views import OrganizationListView, OrganizationDetailHomepageView, \
    OrganizationDetailCourseView, OrganizationDetailIntroduceView, OrganizationDetailTeacherView
from django.views.static import serve
from settings import MEDIA_ROOT
import captcha


urlpatterns = [
    url(r'^xadmin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<register_code>.*)/$', ActiveUserView.as_view(), name='register_code'),
    url(r'forget/$', ForgetPassword.as_view(), name='forget_password'),
    url(r'^reset/(?P<reset_code>[0-9]+)', ResetPassword.as_view(), name='reset_code'),
    url(r'^reset_password/$', SetPasswordView.as_view(), name='reset_password'),

    # 课程机构列表
    url(r'^organization_list/$', OrganizationListView.as_view(), name='organization_list'),
    url(r'^organization_detail_homepage/(?P<org_id>\d+)/$', OrganizationDetailHomepageView.as_view(),
        name='organization_detail_homepage'),
    url(r'^organization_detail_course/(?P<org_id>\d+)/$', OrganizationDetailCourseView.as_view(),
        name='organization_detail_course'),
    url(r'^organization_detail_teachers/(?P<org_id>\d+)/$', OrganizationDetailTeacherView.as_view(),
        name='organization_detail_teachers'),
    url(r'^organization_detail_introduce/(?P<org_id>\d+)/$', OrganizationDetailIntroduceView.as_view(),
        name='organization_detail_introduce'),

    # 课程列表
    url('^course/', include('courses.urls', namespace="course")),

    # 配置media文件路径
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),  # 固定字段document
]

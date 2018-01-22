# -*- coding: utf-8 -*-


from django.conf.urls import url
from .views import CourseView, CourseDetailView, TeacherDetailView, TeacherListView, VideoView, CommentView


urlpatterns = [
    url('^course_list/$', CourseView.as_view(), name='course_list'),
    url('^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url('^course_video/(?P<course_id>\d+)/$', VideoView.as_view(), name='course_video'),
    url('^course_comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    url('^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    url('^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail')
]


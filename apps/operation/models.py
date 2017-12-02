# -*- encoding=utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from users.models import UserWrapper
from courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course = models.CharField(max_length=50, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'user_ask'
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程外键')
    user = models.ForeignKey(UserWrapper, verbose_name=u'用户外键')
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'course_comment'
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程外键')
    favorite_id = models.IntegerField(default=0, verbose_name=u'数据ID')
    favorite_type = models.CharField(choices=(('1', u'课程'), ('2', u'讲师'), ('3', u'课程机构')),
                                     verbose_name=u'收藏类型', max_length=2)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'user_favorite'
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user_id = models.IntegerField(default=0, verbose_name=u'用户ID')
    message = models.CharField(max_length=500, verbose_name=u'用户消息')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'user_message'
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程外键')
    user = models.ForeignKey(UserWrapper, verbose_name=u'用户外键')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'user_course'
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name
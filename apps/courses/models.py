# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    course_describe = models.CharField(max_length=500, verbose_name=u'课程描述')
    course_detail = models.TextField(verbose_name=u'课程详情')
    course_degree = models.CharField(max_length=10, choices=(('height', u'高级'), ('middle', u'中级'), ('low', u'低级')),
                                     verbose_name=u'课程难度')
    learn_time = models.IntegerField(verbose_name=u'学习时长', default=0)
    student = models.IntegerField(verbose_name=u'学生人数')
    image = models.ImageField(verbose_name=u'课程图片', upload_to='course/%Y/%m')
    fav_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    students = models.IntegerField(verbose_name=u'学习人数')
    click_nums = models.IntegerField(verbose_name=u'点击次数')
    add_time = models.DateTimeField(verbose_name=u'课程开始时间', default=datetime.datetime.now)

    class Meta:
        db_table = 'course'
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.course_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程外键')
    name = models.CharField(verbose_name=u'章节名', max_length=50)
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'lesson'
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    course = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(verbose_name=u'视频名', max_length=50)
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'video'
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(verbose_name=u'资料名字', max_length=100)
    download = models.FileField(verbose_name=u'下载地址', upload_to='course/resource/%Y/%m', max_length=200)
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'course_resource'
        verbose_name = u'课程资料'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

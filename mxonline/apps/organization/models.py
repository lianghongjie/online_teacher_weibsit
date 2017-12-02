# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    describe = models.CharField(max_length=200, verbose_name=u'描述')

    class Meta:
        db_table = 'city'
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


class CourseOrganization(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    describe = models.CharField(max_length=200, verbose_name=u'机构描述')
    click_nums = models.IntegerField(verbose_name=u'点击次数')
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    image = models.ImageField(verbose_name=u'机构图片', upload_to='organization/%Y/%m')
    address = models.CharField(max_length=200, verbose_name=u'机构地址')
    city = models.ForeignKey(City, verbose_name=u'城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table = 'course_organization'
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'教师姓名')
    work_year = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=200, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=200, verbose_name=u'工作职位')
    points = models.CharField(max_length=200, verbose_name=u'教学特点')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    click_nums = models.IntegerField(verbose_name=u'点击次数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    organization = models.ForeignKey(CourseOrganization, verbose_name=u'所属机构')

    class Meta:
        db_table = 'teacher'
        verbose_name = u'教师'
        verbose_name_plural = verbose_name


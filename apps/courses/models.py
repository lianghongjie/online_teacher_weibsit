# -*- coding: utf-8 -*-

from django.db import models
import datetime
from organization.models import CourseOrganization, Teacher

# Create your models here.


class Course(models.Model):
    organization = models.ForeignKey(CourseOrganization, verbose_name=u'课程机构外键')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    course_describe = models.CharField(max_length=500, verbose_name=u'课程描述')
    course_detail = models.TextField(verbose_name=u'课程详情')
    course_degree = models.CharField(max_length=10, choices=(('height', u'高级'), ('middle', u'中级'), ('low', u'低级')),
                                     verbose_name=u'课程难度')
    learn_time = models.IntegerField(verbose_name=u'学习时长', default=0)
    image = models.ImageField(verbose_name=u'课程图片', upload_to='course/%Y/%m')
    fav_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name=u'点击次数')
    add_time = models.DateTimeField(verbose_name=u'课程开始时间', default=datetime.datetime.now)
    students = models.IntegerField(verbose_name=u'学习人数', default=0)
    tag = models.CharField(verbose_name=u'tag', default='', max_length=20)
    course_base = models.CharField(verbose_name=u'课程须知', max_length=100, default='')
    what_learn = models.CharField(verbose_name=u'课程你能学到什么', max_length=100, default='')

    teacher = models.ForeignKey(Teacher, verbose_name=u'教师外建', default='')

    class Meta:
        db_table = 'course'
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.course_name

    def get_all_lessons(self):
        return self.lesson_set.all()

    def get_all_students(self):
        return self.student_set.all()


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


class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    phone = models.CharField(max_length=11, verbose_name=u'手机号')
    address = models.CharField(max_length=50, verbose_name=u'地址')
    course = models.ForeignKey(Course, verbose_name=u'课程外建', default='')

    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from .models import Course, CourseResource
from operation.models import CourseComments, UserCourse
from organization.models import Teacher
from utils.mixin import CustomLoginRequestedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from organization.views import _page_object


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')
        return render(request, template_name='course-list.html', context={
            'all_courses': all_courses,
            'hot_courses': hot_courses,
            'sort': sort
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        tag_courses = Course.objects.filter(tag=course.tag)[:3]
        return render(request, template_name='course-detail.html', context={
            'course': course,
            'course_id': course_id,
            'tag_courses': tag_courses
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        organization = teacher.organization
        hot_teachers = TeacherListView.hot_teacher()[:3]
        return render(request, template_name='teacher-detail.html', context={
            'teacher': teacher,
            'teacher_id': teacher_id,
            'organization': organization,
            'hot_teachers': hot_teachers
        })


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_number = all_teachers.count()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        page_obj = _page_object(request, model_object=all_teachers)
        hot_teachers = self.hot_teacher()[:3]
        return render(request, template_name='teachers-list.html', context={
            'page_obj': page_obj,
            'teacher_number': teacher_number,
            'hot_teachers': hot_teachers,
            'sort': sort
        })

    @staticmethod
    def hot_teacher(filed_name='click_nums', order='desc'):
        all_teachers = Teacher.objects.all()
        filed_name if order == 'ordering' else '-{}'.format(filed_name)
        sort_all_teachers = all_teachers.order_by(filed_name)
        return sort_all_teachers


class VideoView(CustomLoginRequestedMixin, View):
    def get(self, request, course_id):
        # 登陆设置, 查询用户是否与课程关联
        # user_courses = UserCourse.objects.filter(course_id=course_id)
        # user_ids = [user_course.user.id for user_course in user_courses]
        # related_user = user_courses.filter(user_id__in=user_ids)
        related_user_course = UserCourse.objects.filter(user=request.user, course_id=course_id)
        if not related_user_course:
            related_user_course = UserCourse()
            related_user_course.user = request.user  # --->related_user_course = UserCourse(user=request.user, course_id=course_id)
            related_user_course.course_id = course_id  # --->related_user_course.save
            related_user_course.save()
        course = Course.objects.get(id=course_id)
        lessons = course.lesson_set.all()
        resources = course.courseresource_set.all()
        teacher = course.teacher
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(
            user_id__in=user_ids)  # user_ids必须是一个序列, user_id__in找出所有user_id在user_ids列表中
        course_ids = [user_course.course.id for user_course in all_user_courses]
        courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        # related_courses = Course.objects.filter(tag=course.tag)
        return render(request, template_name='course-video.html', context={
            'course': course,
            'course_id': course_id,
            'lessons': lessons,
            'resources': resources,
            'teacher': teacher,
            'related_courses': courses
        })


class CommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        teacher = course.teacher
        comments = course.coursecomments_set.all()
        lessons = course.lesson_set.all()
        resources = course.courseresource_set.all()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(
            user_id__in=user_ids)  # user_ids必须是一个序列, user_id__in找出所有user_id在user_ids列表中
        course_ids = [user_course.course.id for user_course in all_user_courses]
        courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        # related_courses = Course.objects.filter(tag=course.tag)
        return render(request, template_name='course-comment.html', context={
            'course_id': course_id,
            'teacher': teacher,
            'comments': comments,
            'course': course,
            'lessons': lessons,
            'resources': resources,
            'related_courses': courses
        })

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CourseOrganization, City, Teacher


class CityAdmin(admin.ModelAdmin):
    pass


class TeacherAdmin(admin.ModelAdmin):
    pass


class CourseOrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseOrganization, CourseOrganizationAdmin)

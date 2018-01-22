from .models import City, CourseOrganization, Teacher
import xadmin


class CityXadmin(object):
    pass


class CourseOrganizationXadmin(object):
    pass


class TeacherXadmin(object):
    pass


xadmin.site.register(City, CityXadmin)
xadmin.site.register(CourseOrganization, CourseOrganizationXadmin)
xadmin.site.register(Teacher, TeacherXadmin)

import xadmin
from .models import Course, CourseResource, Lesson, Video, Student


class CourseXadmin(object):
    pass


class CourseResourceXadmin(object):
    pass


class LessonXadmin(object):
    pass


class VideoXadmin(object):
    pass


class StudentXadmin(object):
    pass


xadmin.site.register(Course, CourseXadmin)
xadmin.site.register(CourseResource, CourseResourceXadmin)
xadmin.site.register(Lesson, LessonXadmin)
xadmin.site.register(Video, VideoXadmin)
xadmin.site.register(Student, StudentXadmin)
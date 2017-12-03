import xadmin
from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskXadmin(object):
    pass


class CourseCommentsXadmin(object):
    pass


class UserFavoriteXadmin(object):
    pass


class UserMessageXadmin(object):
    pass


class UserCourseXadmin(object):
    pass


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(CourseComments, CourseCommentsXadmin)
xadmin.site.register(UserFavorite, UserFavoriteXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
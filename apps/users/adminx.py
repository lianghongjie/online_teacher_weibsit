# -*- encoding=utf-8 -*-
import xadmin
from .models import EmailCode, Banner
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u'慕学网教育平台管理系统'
    site_footer = u'我的第一个网站'
    menu_style = 'accordion'


class EmailCodeXadmin(object):
    pass


class BannerXadmin(object):
    pass


xadmin.site.register(EmailCode, EmailCodeXadmin)
xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

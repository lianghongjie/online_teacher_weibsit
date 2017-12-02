import xadmin
from .models import EmailCode, Banner


class EmailCodeXadmin(object):
    pass


class BannerXadmin(object):
    pass


xadmin.site.register(EmailCode, EmailCodeXadmin)
xadmin.site.register(Banner, BannerXadmin)

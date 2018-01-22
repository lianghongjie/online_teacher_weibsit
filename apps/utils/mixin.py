# -*- coding: utf-8 -*-

# django.conf用于存放配置信息 django.contrib用来存放一般工具

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CustomLoginRequestedMixin(object):  # 自定义方法或类装饰器method_decorator(函数装饰器login_required(login_url))

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CustomLoginRequestedMixin, self).dispatch(request, *args, **kwargs)

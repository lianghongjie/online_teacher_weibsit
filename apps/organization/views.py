# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from .models import CourseOrganization, City
from django.shortcuts import render
import pure_pagination
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrganizationListView(View):
    def get(self, request):
        all_organization = CourseOrganization.objects.all()
        org_count = all_organization.count()
        all_city = City.objects.all()

        # 筛选出请求的数据根据request GET中的?city=1&type=2
        city_id = request.GET.get('city')
        if city_id is not None:
            city_match_orgs = CourseOrganization.objects.filter(city_id=int(city_id))
        else:
            city_match_orgs = all_organization
        page_obj = _page_object(request, model_object=city_match_orgs)
        return render(request, template_name='org-list.html', context={
            'page_obj': page_obj,
            'all_city': all_city,
            'org_count': org_count,
            'city_id': city_id
        })

    def post(self, request):
        pass


def _page_object(request, model_object):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(model_object, 2, request=request)
    page_obj = p.page(page)
    return page_obj
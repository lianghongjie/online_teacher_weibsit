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

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_organization, 3, request=request)

        orgs = p.page(page)

        org_count = all_organization.count()
        all_city = City.objects.all()
        return render(request, template_name='org-list.html', context={
            'all_organization': orgs,
            'all_city': all_city,
            'org_count': org_count
        })

    def post(self, request):
        pass
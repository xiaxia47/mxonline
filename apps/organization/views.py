# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
# Create your views here.


class OrgView(View):
    template_name = 'org-list.html'

    def get(self, request):
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=city_id)
            all_cities = CityDict.objects.all()
        else:
            all_orgs = CourseOrg.objects.all()
            all_cities = CityDict.objects.all()

        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        page_content = Paginator(all_orgs, per_page=4, request=request)
        orgs_list = page_content.page(number=page)

        context = {
            'orgs_list': orgs_list,
            'all_cities': all_cities,
            'org_nums': org_nums,
        }
        return render(request, context=context)

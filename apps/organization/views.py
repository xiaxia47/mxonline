# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict
from operation.forms import UserAskForm
# Create your views here.


class OrgView(View):
    template_name = 'orgs/org-list.html'

    def get(self, request):
        ua = UserAskForm()
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', "")
        sort = request.GET.get('sort','')
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        page_content = Paginator(all_orgs, per_page=4)
        orgs_list = page_content.page(number=page)

        context = {
            'orgs_list': orgs_list,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city': city_id,
            'ct': category,
            'hot_orgs': hot_orgs,
            'sorted': sort,
            'ua_form': ua,
        }
        return render(request, context=context, template_name=self.template_name)

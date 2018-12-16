# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict
from operation.forms import UserAskForm
from operation.models import UserFavorite
# Create your views here.

COURSE_FAV = 2


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
            'cur_page': 'org_list',
        }

        return render(request, context=context, template_name=self.template_name)


class OrgHomeView(View):
    template_name = 'orgs/org-detail-homepage.html'
    url_path = ''

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=COURSE_FAV)
            if existed_rec:
                has_fav = True
        course_org = CourseOrg.objects.get(id=org_id)
        context = {
            'has_fav': has_fav,
            'org_id':org_id,
            'courses':course_org.course_set.all()[:3],
            'teachers':course_org.teacher_set.all()[:1],
            'course_org':course_org,
            'cur_page':'home',
        }
        return render(request, template_name=self.template_name, context=context)


class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    template_name = 'orgs/org-detail-course.html'
    url_path = ''

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=COURSE_FAV)
            if existed_rec:
                has_fav = True
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        page_content = Paginator(all_courses, per_page=9)
        courses_list = page_content.page(number=page)
        context = {
            'has_fav': has_fav,
            'org_id': org_id,
            'course_org': course_org,
            'courses': courses_list,
            'cur_page': 'course',
        }
        return render(request, template_name=self.template_name, context=context)


class OrgDescView(View):
    '''
    机构介绍
    '''
    template_name = 'orgs/org-detail-desc.html'
    url_path = ''

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=COURSE_FAV)
            if existed_rec:
                has_fav = True
        course_org = CourseOrg.objects.get(id=org_id)
        context = {
            'has_fav': has_fav,
            'org_id': org_id,
            'course_org': course_org,
            'cur_page': 'desc',
        }
        return render(request, template_name=self.template_name, context=context)


class OrgTeacherView(View):
    '''
    机构教师
    '''
    template_name = 'orgs/org-detail-teachers.html'
    url_path = ''

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=COURSE_FAV)
            if existed_rec:
                has_fav = True
        course_org = CourseOrg.objects.get(id=org_id)
        teachers = course_org.teacher_set.all()
        context = {
            'has_fav': has_fav,
            'org_id': org_id,
            'course_org': course_org,
            'teachers': teachers,
        }
        return render(request, template_name=self.template_name, context=context)
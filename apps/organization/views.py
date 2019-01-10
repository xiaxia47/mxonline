# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from MxOnline.settings import FAV_TYPE
from operation.forms import UserAskForm
from operation.models import UserFavorite
# Create your views here.



class OrgListView(View):
    template_name = 'orgs/org-list.html'

    def get(self, request):
        ua = UserAskForm()
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', '')
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', "")
        sort = request.GET.get('sort', '')

        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                             Q(address__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords)).distinct()
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
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=FAV_TYPE['course'])
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
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=FAV_TYPE['course'])
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
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=FAV_TYPE['course'])
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
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=FAV_TYPE['course'])
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


class TeacherListView(View):
    '''
    机构教师
    '''
    template_name = 'orgs/teachers-list.html'
    url_path = ''

    def get(self, request):
        teachers = Teacher.objects.all()
        hot_teachers = teachers.order_by('-click_nums')[:5]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            teachers = teachers.filter(Q(name__icontains=search_keywords)
                                       |Q(course__name__icontains=search_keywords)
                                       |Q(org__name__icontains=search_keywords)).distinct()
        teacher_cnt = teachers.count()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-fav_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        page_content = Paginator(teachers, per_page=4)
        teachers_list = page_content.page(number=page)

        context = {
            'teachers_list': teachers_list,
            'teacher_cnt': teacher_cnt,
            'hot_teachers': hot_teachers,
            'sort': sort,
            'cur_page': '',
        }
        return render(request, template_name=self.template_name, context=context)


class TeacherDetailView(View):
    '''
    机构教师
    '''
    template_name = 'orgs/teacher-detail.html'
    url_path = ''

    def get(self, request, teacher_id):
        has_fav_org, has_fav_teacher = False, False
        teacher = Teacher.objects.get(id=teacher_id)
        hot_teachers = Teacher.objects.order_by('-click_nums')[:5]
        courses = teacher.course_set.all()
        org = teacher.org
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=FAV_TYPE['corg'])
            if existed_rec:
                has_fav_org = True
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=FAV_TYPE['teacher'])
            if existed_rec:
                has_fav_teacher = True
        context = {
            'has_fav_org': has_fav_org,
            'has_fav_teacher': has_fav_teacher,
            'hot_teachers': hot_teachers,
            'courses': courses,
            'course_org': org,
            'teacher': teacher,
        }
        return render(request, template_name=self.template_name, context=context)


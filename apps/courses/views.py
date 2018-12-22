from django.shortcuts import render
from django.views.generic.base import View

from django.core.paginator import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite
from MxOnline.settings import ORG_FAV, COURSE_FAV
# Create your views here.


class CourseListView(View):
    cur_page = 'course_list'
    template_name = 'courses/course-list.html'

    def get(self, request):
        all_courses = Course.objects.all()
        sort_type = request.GET.get('sort', '')
        hot_courses = all_courses.order_by('-click_nums')
        if sort_type == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort_type == 'hot':
            all_courses = hot_courses
        hot_courses = hot_courses[:3]
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1
        page_content = Paginator(all_courses, per_page=8)
        courses_list = page_content.page(number=page)

        context = {
            'courses_list': courses_list,
            'hot_courses': hot_courses,
            'cur_page': self.cur_page,
            'sort': sort_type,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CourseDetailView(View):
    '''
    课程详情页
    '''
    cur_page = 'courseDetail'
    template_name = 'courses/course-detail.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        company = course.course_org
        if course.tag:
            relate_courses = Course.objects.filter(tag=course.tag).exclude(id=course.id).order_by("students")[:2]
        else:
            relate_courses = []
        has_fav_org = has_fav_course = False
        if request.user.is_authenticated:
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=COURSE_FAV)
            if existed_rec:
                has_fav_course = True
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=company.id, fav_type=ORG_FAV)
            if existed_rec:
                has_fav_org = True
        context = {
            'has_fav_org': has_fav_org,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'course': course,
            'company': company,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CourseCommentView(View):

    cur_page = 'courseComment'
    template_name = 'courses/course-comment.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        comment_list = course.coursecomment_set.all().order_by("-add_time")
        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'comment_list': comment_list,
            'course_resources': all_resources,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CourseVideoView(View):

    cur_page = 'courseVideo'
    template_name = 'courses/course-video.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_resources,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)

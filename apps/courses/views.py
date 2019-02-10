from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, UserCourse
from MxOnline.settings import FAV_TYPE
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    cur_page = 'course_list'
    template_name = 'courses/course-list.html'

    def get(self, request):
        all_courses = Course.objects.all().order_by('add_time')

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(teacher__name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords)).distinct()
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
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=FAV_TYPE['course'])
            if existed_rec:
                has_fav_course = True
            existed_rec = UserFavorite.objects.filter(user=request.user, fav_id=company.id, fav_type=FAV_TYPE['corg'])
            if existed_rec:
                has_fav_org = True
        context = {
            'has_fav_org': has_fav_org,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'course': course,
            'company': company,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CourseCommentView(LoginRequiredMixin, View):

    cur_page = 'courseComment'
    template_name = 'courses/course-comment.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        user_courses = UserCourse.objects.filter(id=course_id)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)

        course_ids = [course.id for course in all_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        comment_list = course.coursecomment_set.all().order_by("-add_time")
        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'related_courses': related_courses,
            'comment_list': comment_list,
            'course_resources': all_resources,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CourseVideoView(LoginRequiredMixin, View):

    cur_page = 'courseVideo'
    template_name = 'courses/course-video.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(course=course, user=request.user)
            user_course.save()
            course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(id=course_id)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.id for course in all_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        context = {
            'course': course,
            'related_courses': related_courses,
            'course_resources': all_resources,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)


class CoursePlayView(LoginRequiredMixin, View):

    cur_page = 'coursePlay'
    template_name = 'courses/course-play.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        course = video.lesson.course
        course.click_nums += 1
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(course=course, user=request.user)
            user_course.save()
            course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(id=course.id)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.id for course in all_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        context = {
            'course': course,
            'video': video,
            'related_courses': related_courses,
            'course_resources': all_resources,
            'cur_page': self.cur_page,
        }
        return render(request=request, template_name=self.template_name, context=context)

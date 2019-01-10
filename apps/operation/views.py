import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .forms import UserAskForm
from .models import UserFavorite, CourseComment
from courses.models import Course, CourseOrg, Teacher
from MxOnline.settings import FAV_TYPE
# Create your views here.


class AddUserAskView(View):

    def post(self, request):
        ua_form = UserAskForm(request.POST)
        context = {}
        if ua_form.is_valid():
            ua_form.save(commit=True)
            context['status'] = 'success'
            context['msg'] = '成功添加，请等待通知'
        else:
            context['status'] = 'fail'
            context['msg'] = list(ua_form.errors.values())[0]
        return HttpResponse(content=json.dumps(context), content_type='application/json')


class AddUserFavView(View):
    '''
    用户收藏以及取消收藏
    @fav_type 1- 收藏课程  2 - 收藏机构  3 - 收集教师
    '''

    def chg_fav(self, fav_id, fav_type, cnt):
        try:
            if fav_type == 'course':
                course = Course.objects.get(id=fav_id)
                course.fav_nums += cnt
                course.save()
            elif fav_type == 'corg':
                courseOrg = CourseOrg.objects.get(id=fav_id)
                courseOrg.fav_nums += cnt
                courseOrg.save()
            elif fav_type == 'teacher':
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums += cnt
                teacher.save()
        except Exception as e:
            print(e)
            return False
        return True

    def post(self, request):
        context = {}
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = request.POST.get('fav_type', '')
        if not request.user.is_authenticated:
            context['status'] = 'fail'
            context['msg'] = '用户未登录'
            return HttpResponse(content=json.dumps(context), content_type='application/json')
        user = request.user
        existed_rec = UserFavorite.objects.filter(user=user, fav_id=fav_id, fav_type=FAV_TYPE[fav_type])
        if existed_rec:
            existed_rec.delete()
            status = self.chg_fav(fav_id, fav_type, -1)
            context['status'] = 'success'
            if status:
                context['msg'] = '取消收藏成功'
            else:
                context['msg'] = '取消收藏成功，计数器失败'
        elif fav_id > 0 and fav_type in FAV_TYPE.keys():
            user_fav = UserFavorite(user=user, fav_id=fav_id, fav_type=FAV_TYPE[fav_type])
            user_fav.save()
            status = self.chg_fav(fav_id, fav_type, 1)
            context['status'] = 'success'
            if status:
                context['msg'] = '收藏成功'
            else:
                context['msg'] = '收藏成功，计数器失败'
        else:
            context['status'] = 'fail'
            context['msg'] = '收藏出错'
        return HttpResponse(content=json.dumps(context), content_type='application/json')


class AddCourseComment(View):
    '''
    用户收藏以及取消收藏
    @fav_type 1- 收藏课程  2 - 收藏机构  3 - 收藏教师
    '''
    def post(self, request):
        done = False
        context = {}
        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', "")
        if not request.user.is_authenticated:
            context['status'] = 'fail'
            context['msg'] = '用户未登录'
            done = True
        user = request.user
        if done:
            pass
        elif course_id <= 0 or not Course.objects.all().get(id=course_id):
            context['status'] = 'fail'
            context['msg'] = '不是有效课程'
        elif comments is "":
            context['status'] = 'fail'
            context['msg'] = '请输入评论'
        else:
            new_comment = CourseComment(user=user, course_id=course_id, comments=comments)
            new_comment.save()
            context['status'] = 'success'
            context['msg'] = '评论成功'
        return HttpResponse(content=json.dumps(context), content_type='application/json')

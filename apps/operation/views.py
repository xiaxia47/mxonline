import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .forms import UserAskForm
from .models import UserFavorite
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
    @fav_type 1- 收藏课程  2 - 收藏机构
    '''
    def post(self, request):
        context = {}
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type',''))
        if not request.user.is_authenticated:
            context['status'] = 'fail'
            context['msg'] = '用户未登录'
            return HttpResponse(content=json.dumps(context), content_type='application/json')
        user = request.user
        existed_rec = UserFavorite.objects.filter(user=user, fav_id=fav_id, fav_type=fav_type)
        if existed_rec:
            existed_rec.delete()
            context['status'] = 'success'
            context['msg'] = '已取消收藏'
        elif fav_id > 0 and fav_type > 0:
            user_fav = UserFavorite(user=user, fav_id=fav_id, fav_type=fav_type)
            user_fav.save()
            context['status'] = 'success'
            context['msg'] = '已收藏'
        else:
            context['status'] = 'fail'
            context['msg'] = '收藏出错'
        return HttpResponse(content=json.dumps(context), content_type='application/json')


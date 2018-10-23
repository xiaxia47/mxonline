import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from operation.forms import UserAskForm

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
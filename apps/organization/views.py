# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class OrgView(View):

    def get(self, request):
        return render(request, template_name='org-list.html', context=None)

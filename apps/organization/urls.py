# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/9 9:25'
from django.urls import path

from .views import OrgView

app_name = 'orgs'
urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
]
# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/9 9:25'
from django.urls import path

from .views import OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from .views import TeacherListView, TeacherDetailView

app_name = 'orgs'
urlpatterns = [
    path('list/', OrgListView.as_view(), name='org_list'),
    path('home/<int:org_id>', OrgHomeView.as_view(), name='home'),
    path('course/<int:org_id>', OrgCourseView.as_view(), name='course'),
    path('desc/<int:org_id>', OrgDescView.as_view(), name='desc'),
    path('org_teacher/<int:org_id>', OrgTeacherView.as_view(), name='teacher'),
    path('desc/<int:org_id>', OrgDescView.as_view(), name='desc'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>', TeacherDetailView.as_view(), name='teacher_detail'),
]
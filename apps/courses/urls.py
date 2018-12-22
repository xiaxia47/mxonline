# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/11/15 15:31'
from django.urls import path

from .views import CourseListView, CourseCommentView, CourseDetailView, CourseVideoView


app_name = 'courses'
urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='detail'),
    path('comment/<int:course_id>', CourseCommentView.as_view(), name='comment'),
    path('video/<int:course_id>', CourseVideoView.as_view(), name='video'),
]
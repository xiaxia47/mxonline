# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/16 16:50'

from django.urls import path

from .views import AddUserAskView, AddUserFavView, AddCourseCommentView, SendPinCodeView

app_name = 'oper'
urlpatterns = [
    path('addask/', AddUserAskView.as_view(), name='user_ask'),
    path('addfav/', AddUserFavView.as_view(), name='add_fav'),
    path('addCourseComment/', AddCourseCommentView.as_view(), name='add_comment'),
    path('sendpin/', SendPinCodeView.as_view(), name='send_pin')
]


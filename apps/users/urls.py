# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/9 9:33'

from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('pwd_reset/', views.PwdResetView.as_view(), name='pwd_reset'),
    path('activate/<slug:active_code>', views.ActivateUser.as_view(), name='activate'),
    path('forget/', views.ForgetPwdView.as_view(), name='forget'),
    path('reset/<slug:reset_code>', views.ResetView.as_view(), name='reset'),
    path('expired/', TemplateView.as_view(template_name='users/url_expired.html'), name='expired'),
    path('mail_sent/', TemplateView.as_view(template_name='users/send_success.html'), name='mail_sent'),
    # 个人中心
    path('home/', views.UserInfoCenter.as_view(), name='home'),
    # 我的收藏-机构
    path('fav/org/', TemplateView.as_view(template_name='users/send_success.html'), name='favorg'),
    # 我的课程
    path('courses/', views.UserCourseView.as_view(), name='course'),
    # 我的收藏-机构
    path('fav/org/', TemplateView.as_view(template_name='users/send_success.html'), name='favorg'),
    # 我的收藏-机构
    path('fav/org/', TemplateView.as_view(template_name='users/send_success.html'), name='favorg'),
    path('message/', TemplateView.as_view(template_name='users/send_success.html'), name='message'),
    path('uploadimage/', views.UploadImageView.as_view(), name='upload_img'),
    path('update_email/', views.UpdateEmailView.as_view(), name='update_email'),
    path('updatepwd/', views.UpdatePasswordView.as_view(), name='updatepwd'),
]


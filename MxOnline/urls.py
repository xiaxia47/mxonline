"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import include

from users.views import LoginView, RegisterView, ActivateUser, ForgetPwdView, ResetView, PwdResetView
from organization.views import OrgView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('activate/<slug:active_code>', ActivateUser.as_view(), name='activate'),
    path('forget/', ForgetPwdView.as_view(), name='forget'),
    path('reset/<slug:reset_code>', ResetView.as_view(), name='reset'),
    path('pwd_reset/', PwdResetView.as_view(), name='pwd_reset'),
    path('org_list/', OrgView.as_view(), name='org_list'),
]

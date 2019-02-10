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
from django.urls import path, re_path
from django.conf.urls import include
from django.views.static import serve

from .settings import MEDIA_ROOT, DEBUG
from users.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('captcha/', include('captcha.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('orgs/', include('organization.urls', namespace='orgs')),
    path('oper/', include('operation.urls', namespace='oper')),
    path('courses/', include('courses.urls', namespace='courses')),
    re_path('media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    #
]

if not DEBUG:
    from .settings import STATIC_ROOT
    urlpatterns.append(re_path('static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}))



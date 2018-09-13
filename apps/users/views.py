# _*_ coding:utf-8 _*_

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from .models import UserProfile
from .forms import LoginForm

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(raw_password=password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={})

    def post(self, request):
        context = {}
        next_template = self.template_name
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user=user)
                next_template = 'index.html'
            else:
                context['msg'] = '用户名或密码错误'
        else:
            context['login_form'] = login_form
        return render(request=request, template_name=next_template, context=context)

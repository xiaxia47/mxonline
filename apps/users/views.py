# _*_ coding:utf-8 _*_

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_utils import send_register_email, email_is_exist
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username))
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
            if user is not None and user.is_active:
                login(request, user=user)
                next_template = 'index.html'
            else:
                context['msg'] = '用户名密码错误或用户未激活'
        else:
            context['login_form'] = login_form
        return render(request=request, template_name=next_template, context=context)


class RegisterView(View):

    def post(self, request):
        register_form = RegisterForm(request.POST)
        template_name = 'register.html'
        context = {}
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            pass_word = request.POST.get('password', "")
            context['register_form'] = register_form
            if not email_is_exist(UserProfile, user_name):
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.set_password(raw_password=pass_word)
                user_profile.is_active = False
                user_profile.save()
                send_register_email(user_name, 'register')
                context['msg'] = "注册成功，激活链接已发送到您的邮箱"
                template_name = 'login.html'
            else:
                context['msg'] = "该邮箱已被使用"
        else:
            context['register_form'] = register_form

        return render(request, template_name=template_name, context=context)


class ForgetPwdView(View):

    def get(self, request):
        forget_form = ForgetForm()
        context = {'forget_form': forget_form}
        return render(request, template_name='forgetpwd.html', context=context)

    def post(self, request):
        context = {}
        forget_form = ForgetForm(request.POST)
        template_name = 'forgetpwd.html'
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if email_is_exist(UserProfile, email):
                send_register_email(receiver=email, send_type='forget')
                template_name = 'send_success.html'
            else:
                context['forget_form'] = forget_form
                context['msg'] = '账号非法或者不存在'
        else:
            context['forget_form'] = forget_form
        return render(request, template_name=template_name, context=context)


class ActivateUser(View):

    def get(self, request, active_code):
        template_name = "login.html"
        context = {}
        email_rec = EmailVerifyRecord.objects.get(code=active_code)
        if email_rec and email_rec.valid:
            email = email_rec.email
            email_rec.valid = False
            email_rec.save()
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            context['msg'] = '激活成功，请重新登录'
        else:
            template_name = 'url_expired.html'

        return render(request, template_name=template_name, context=context)


class ResetView(View):

    def get(self, request, reset_code):
        template_name = 'url_expired.html'
        context = {}
        email_rec = EmailVerifyRecord.objects.get(code=reset_code)
        if email_rec and email_rec.valid:
            modify_form = ModifyPwdForm(initial={'reset_code':reset_code,'email':email_rec.email})
            context['msg'] = '已经通过验证，请设置新密码,本页面刷新后失效'
            context['modify_form'] = modify_form
            template_name = "password_reset.html"

        return render(request, template_name=template_name, context=context)


class PwdResetView(View):

    def get(self, request):
        template_name = "password_reset.html"
        modify_form = ModifyPwdForm()
        context = {'modify_form': modify_form}
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        template_name = "password_reset.html"
        modify_form = ModifyPwdForm(request.POST)
        context = {'modify_form': modify_form}
        if modify_form.is_valid():
            reset_code = modify_form.data.get('reset_code','')
            email_rec = EmailVerifyRecord.objects.get(code=reset_code)
            if email_rec.valid:
                email_rec.valid = False
                user = UserProfile.objects.get(email=email_rec.email)
                if user and user.is_active:
                    user.set_password(raw_password=modify_form.data.get('new_password', ''))
                    user.save()
                    context['msg'] = '重置成功，请重新登录'
                    template_name = "login.html"
                else:
                    context['msg'] = '用户已注销或不存在'
            else:
                template_name = 'url_expired.html'
        else:
            context['msg'] = '输入有误，请重试'
        return render(request, template_name=template_name, context=context)
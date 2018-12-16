# _*_ coding:utf-8 _*_

from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View,TemplateView

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_utils import send_register_email, email_is_exist
from organization.models import CourseOrg
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

    template_name = 'users/login.html'
    url = 'users:login'

    def get(self, request):
        context = {'login_form': LoginForm()}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request):
        context = {'request': request}
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None and user.is_active:
                login(request, user=user)
                self.url = 'index'
                return redirect(reverse(self.url), kwargs=context)
            else:
                context['msg'] = '用户名密码错误或用户未激活'
        else:
            context['login_form'] = login_form
        return render(request=request, template_name=self.template_name)


class RegisterView(View):
    template_name = 'users/register.html'
    url = 'users:register'

    def get(self, request):
        context = {'register_form': RegisterForm()}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        context = {'request': request}
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
                self.template_name = 'users/login.html'
            else:
                context['msg'] = "该邮箱已被使用"
        else:
            context['register_form'] = register_form

        return render(request=request, template_name=self.template_name, context=context)


class ForgetPwdView(View):

    template_name = 'users/forgetpwd.html'
    url = 'users:forget'

    def get(self, request):
        forget_form = request.GET.get('forget_form', ForgetForm())
        context = {'forget_form': forget_form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        context = {'request': request}
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if email_is_exist(UserProfile, email):
                send_register_email(receiver=email, send_type='forget')
                self.url = 'users:mail_sent'
                return redirect(reverse(self.url))
            else:
                context['forget_form'] = forget_form
                context['msg'] = '账号非法或者不存在'
        else:
            context['forget_form'] = forget_form
        return render(request=request, template_name=self.template_name, context=context)


class ActivateUser(View):

    template_name = 'users/forgetpwd.html'
    url = 'users:activate'

    def get(self, request, active_code):
        context = {'request': request}
        email_rec = EmailVerifyRecord.objects.get(code=active_code)
        if email_rec and email_rec.valid:
            email = email_rec.email
            email_rec.valid = False
            email_rec.save()
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            context['msg'] = '激活成功，请重新登录'
            self.template_name = "users/login.html"
            return render(request=request, template_name=self.template_name, context=context)
        else:
            self.url = 'users:expired'
            return redirect(reverse(self.url))


class ResetView(View):
    template_name = 'users/password_reset.html'
    url = 'users:reset'

    def get(self, request, reset_code):
        context = {'request': request}
        email_rec = EmailVerifyRecord.objects.get(code=reset_code)
        if email_rec and email_rec.valid:
            modify_form = ModifyPwdForm(initial={'reset_code': reset_code, 'email': email_rec.email})
            context['msg'] = '已经通过验证，请设置新密码,本页面刷新后失效'
            context['modify_form'] = modify_form
            return render(request=request, template_name=self.template_name, context=context)
        else:
            self.url = 'users:expired'
        return redirect(reverse(self.url), kwargs=context)


class PwdResetView(View):

    template_name = 'users/password_reset.html'
    url = 'users:pwd_reset'

    def get(self, request):
        modify_form = request.GET.get('modify_form', ModifyPwdForm())
        msg = request.GET.get('msg', '')
        context = {'modify_form': modify_form,
                   'msg': msg
                   }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        context = {'modify_form': modify_form,
                   'request': request}
        if modify_form.is_valid():
            reset_code = modify_form.data.get('reset_code', '')
            email_rec = EmailVerifyRecord.objects.get(code=reset_code)
            if email_rec.valid:
                email_rec.valid = False
                user = UserProfile.objects.get(email=email_rec.email)
                if user and user.is_active:
                    user.set_password(raw_password=modify_form.data.get('new_password', ''))
                    user.save()
                    context['msg'] = '重置成功，请重新登录'
                    email_rec.save()
                    self.template_name = 'users/login.html'
                else:
                    context['msg'] = '用户已注销或不存在'
            else:
                self.template_name = 'users/url_expired.html'
        else:
            context['msg'] = '输入有误，请重试'

        return render(request=request, template_name=self.template_name, context=context)


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        context = {}
        context['org_list'] = CourseOrg.objects.all()[:30]
        context['cur_page'] = 'index'
        return render(request=request, template_name=self.template_name, context=context)

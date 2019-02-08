# _*_ coding:utf-8 _*_

import json

from django.shortcuts import render, reverse, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from MxOnline.settings import FAV_TYPE
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, \
     UploadImageForm, UpdatePwdForm, ModifyEmailForm, ModifyUserForm
from utils.email_utils import send_register_email, email_is_exist
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import Teacher, CourseOrg
from courses.models import Course

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(raw_password=password):
                return user
        except Exception as e:
            print(e)
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
        return render(request=request, template_name=self.template_name, context=context)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


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
                user_message = UserMessage(user=user_profile.id, msg_body='欢迎注册在线学习教育网')
                user_message.save()

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
        #取出轮播图
        banners = Banner.objects.all().order_by('index')[:5]
        courses = Course.objects.all().order_by('fav_nums')[:6]
        banner_courses = Course.objects.filter(is_banner=True).order_by('fav_nums')[:3]

        context = {
            'org_list': CourseOrg.objects.all()[:15],
            'courses': courses,
            'banner_courses': banner_courses,
            'cur_page': 'index',
            'banners': banners,
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserInfoCenter(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    template_name = 'users/usercenter-info.html'
    url = 'users:home'

    def get(self, request):
        image_form = UploadImageForm()
        context = {'image_form': image_form}
        return render(request, context=context, template_name=self.template_name)

    def post(self, request):
        user_info = ModifyUserForm(request.POST, instance=request.user)
        context = {}
        if user_info.is_valid():
            user_info.save()
            context['status'] = 'success'
            context['msg'] = '资料更改成功'
        else:
            context['status'] = 'fail'
            context['msg'] = list(user_info.errors.values())[0]
        return HttpResponse(content=json.dumps(context), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        context = {}
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save(commit=True)
            context['status'] = 'success'
            context['msg'] = '头像更改成功'
        else:
            context['status'] = 'fail'
            context['msg'] = list(image_form.errors.values())[0]
        return HttpResponse(content=json.dumps(context), content_type='application/json')


class UpdatePasswordView(View):

    def post(self, request):
        modify_form = UpdatePwdForm(request.POST)
        context = {}
        if modify_form.is_valid():
            request.user.set_password(raw_password=modify_form.cleaned_data.get('new_password', ''))
            request.user.save()
            context['msg'] = '重置成功，请重新登录'
            context['status'] = 'success'
        else:
            context = json.dumps(modify_form.errors)
        context = json.dumps(context)
        return HttpResponse(content=context, content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):


    def post(self, request):
        modify_form = ModifyEmailForm(request.POST)
        context = {}
        if modify_form.is_valid():
            email, code = modify_form.cleaned_data['email'], modify_form.cleaned_data['code']
            email_rec = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='pincode')
            if email_rec.count() > 0 and email_rec[0].is_valid():
                request.user.email = email
                request.user.save()
                context['msg'] = '邮箱更新成功'
                context['status'] = 'success'
            else:
                context['msg'] = '验证码失效或者邮箱地址无效，请重试'
                context['status'] = 'failed'
        else:
            context['msg'] = str(modify_form.errors['email'][0])
            context['status'] = 'failed'
        context = json.dumps(context)
        return HttpResponse(content=context, content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    template_name = 'users/usercenter-mycourse.html'

    def get(self, request):
        courses = UserCourse.objects.filter(user=request.user)
        context = {
            'courses': courses
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserFavCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    template_name = 'users/usercenter-fav-course.html'

    def get(self, request):
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type=FAV_TYPE['course'])
        courses = Course.objects.filter(id__in=[favrec.fav_id for favrec in fav_ids])
        context = {
            'fav_courses': courses
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserFavOrgView(LoginRequiredMixin, View):
    '''
    收藏-我的机构
    '''
    template_name = 'users/usercenter-fav-org.html'

    def get(self, request):
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type=FAV_TYPE['corg'])
        orgs = CourseOrg.objects.filter(id__in=[favrec.fav_id for favrec in fav_ids])
        context = {
            'fav_orgs': orgs
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserFavTeacherView(LoginRequiredMixin, View):
    '''
    收藏-我的教师
    '''
    template_name = 'users/usercenter-fav-teacher.html'

    def get(self, request):
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type=FAV_TYPE['teacher'])
        teachers = Teacher.objects.filter(id__in=[favrec.fav_id for favrec in fav_ids])
        context = {
            'fav_teachers': teachers
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserMessageView(LoginRequiredMixin, View):
    '''
    消息中心
    '''

    template_name = 'users/usercenter-message.html'

    def get(self, request):
        messages = UserMessage.objects.filter(user__in=[0, request.user.id])
        unread_messages = UserMessage.objects.filter(user__in=[request.user.id], has_read=False)
        for msg in unread_messages.all():
            msg.has_read = True
            msg.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        page_content = Paginator(messages, per_page=4)
        messages = page_content.page(number=page)

        context = {
            'user_messages': messages
        }
        return render(request=request, template_name=self.template_name, context=context)


def page_not_found(request, template_name='404.html'):
    from django.shortcuts import render_to_response
    response = render_to_response(template_name=template_name, context='')
    response.status_code = 404
    return response

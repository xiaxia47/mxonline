# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/13 14:01'

import re

from django import forms
from captcha.fields import CaptchaField
from django.forms import HiddenInput

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, initial='')
    password = forms.CharField(required=True, initial='', min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ModifyUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'email']
        widgets = {
            'nick_name': forms.TextInput(attrs={'placeholder': '昵称'}),
            'birthday': forms.SelectDateWidget(attrs={'placeholder': '生日','required':True}),
            'gender': forms.TextInput(attrs={'placeholder': '性别'}),
            'address': forms.TextInput(attrs={'placeholder': '地址'}),
            'mobile': forms.TextInput(attrs={'placeholder': '手机号'}),
            'email': forms.EmailInput(attrs={'placeholder': '电子邮件'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.match(r'^1\d{10}$', mobile):
            raise forms.ValidationError('手机号非法', code='mobile_invalid')
        return mobile


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdatePwdForm(forms.Form):
    old_password = forms.CharField(required=True, min_length=6, max_length=20, widget=forms.PasswordInput())
    new_password = forms.CharField(required=True, min_length=6, max_length=20, widget=forms.PasswordInput())

    def clean_new_password(self):
        old_pwd = self.cleaned_data.get('old_password')
        new_pwd = self.cleaned_data.get('new_password')
        if old_pwd != new_pwd:
            raise forms.ValidationError('两次输入密码不一致，请重新输入')
        return new_pwd


class ModifyPwdForm(UpdatePwdForm):
    email = forms.EmailField(required=True, widget=HiddenInput())
    reset_code = forms.CharField(required=True, max_length=20, widget=HiddenInput())


class ModifyEmailForm(forms.Form):
    email = forms.EmailField(required=True, widget=HiddenInput())
    code = forms.CharField(required=True, max_length=20, widget=HiddenInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('邮箱已经被占用')
        else:
            return email


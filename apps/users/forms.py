# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/13 14:01'

from django import forms
from captcha.fields import CaptchaField
from django.forms import HiddenInput

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ModifyPwdForm(forms.Form):
    email = forms.EmailField(required=True, widget=HiddenInput())
    old_password = forms.CharField(required=True, min_length=6, max_length=20, widget=forms.PasswordInput())
    new_password = forms.CharField(required=True, min_length=6, max_length=20, widget=forms.PasswordInput())
    reset_code = forms.CharField(required=True, max_length=20, widget=HiddenInput())

    def clean_new_password(self):
        old_pwd = self.cleaned_data.get('old_password')
        new_pwd = self.cleaned_data.get('new_password')
        if old_pwd != new_pwd:
            raise forms.ValidationError('两次输入密码不一致，请重新输入')
        return new_pwd

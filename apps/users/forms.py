# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/13 14:01'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True,)
    password = forms.CharField(required=True, min_length=5)

# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/10/16 16:44'
import re

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '姓名'}),
            'mobile': forms.TextInput(attrs={'placeholder': '手机号'}),
            'course_name': forms.TextInput(attrs={'placeholder': '课程名'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.match(r'^1\d{10}$', mobile):
            raise forms.ValidationError('手机号非法', code='mobile_invalid')
        return mobile
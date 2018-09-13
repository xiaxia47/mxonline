from django.shortcuts import render,reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import  ModelBackend

from .models import UserProfile
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password=password):
                return user
        except Exception as e:
            return None


def user_login(request):
    next_template = 'login.html'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user=user)
            next_template = 'index.html'
    return render(request=request, template_name=next_template, context={})

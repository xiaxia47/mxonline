from datetime import datetime

#第三方
from django.db import models
from django.contrib.auth.models import AbstractUser

#自定义lib
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female")
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)

    class Meta:
        verbose_name_plural = verbose_name = "用户信息"

    def __str__(self):
        return self.self


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register","注册"), ("forget","找回密码")), max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = verbose_name = "邮箱验证码"


class PageBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name="轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name_plural = verbose_name = "轮播图"

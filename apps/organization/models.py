# _*_ coding:utf-8 _*_
from django.db import models
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = verbose_name = "城市"

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构简介")
    category = models.CharField(max_length=20,
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')),
                                verbose_name='机构类别',
                                default='pxjg')
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图", null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name="所在城市", on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = verbose_name = "课程机构"

    def __str__(self):
        return self.name

    #获取教师数量
    def get_teacher_total(self):
        return self.teacher_set.all().count()

    #获取课程数量
    def get_course_total(self):
        return self.course_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="公司名称")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    is_verified = models.BooleanField(verbose_name='是否认证', default=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    image = models.ImageField(verbose_name="头像", upload_to="teachers/%Y/%m", max_length=100,
                              null=True, blank=True, default='')
    age = models.CharField(max_length=3, verbose_name="年龄", null=True, default='18', blank=True)
    fav_nums = models.IntegerField(default=0, verbose_name="收藏")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = verbose_name = "教师"

    def __str__(self):
        return f"{self.org}-{self.name}"

    def get_course_count(self):
        return self.course_set.count()

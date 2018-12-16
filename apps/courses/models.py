# _*_ coding:utf-8 _*-
from datetime import datetime
from django.db import models

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name='授课教师', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name="课程难度", max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏")
    image = models.ImageField(verbose_name="封面图", upload_to="courses/%Y/%m", max_length=100, null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    tag = models.CharField(default='', verbose_name="课程标签", max_length=10)
    add_time = models.DateTimeField(default=datetime.now,verbose_name="课程添加时间")

    class Meta:
        verbose_name_plural = verbose_name = "课程"

    #获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    #获取当前的学生
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = verbose_name_plural = "章节"

    def __str__(self):
        return f"{self.course}-{self.name}"


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = verbose_name_plural = "视频"

    def __str__(self):
        return f"{self.lesson}-{self.name}"


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = verbose_name_plural = "课程资源"

    def __str__(self):
        return f"{self.course}-{self.name}"
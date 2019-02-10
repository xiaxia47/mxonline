# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/10 14:07'


import xadmin

from .models import *


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourseInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times',
                    'students', 'image', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times',
                     'students', 'image', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times',
                   'students', 'image', 'fav_nums', 'click_nums', 'add_time']
    ordering = ['-click_nums', 'students']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']  # 后台不显示 字段与readonly_fields 冲突，不可重复
    inlines = [LessonInline, CourseResourseInline]  # 当前页配置关联内容
    style_fields = {'detail': 'ueditor'} #制定样式
    list_editable = ['degree', 'name']
    enable_import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        return qs.filter(is_banner=False)

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times',
                    'students', 'image', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times',
                     'students', 'image', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times',
                   'students', 'image', 'fav_nums', 'click_nums', 'add_time']
    ordering = ['-click_nums', 'students']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']  # 后台不显示 字段与readonly_fields 冲突，不可重复
    inlines = [LessonInline, CourseResourseInline]  # 当前页配置关联内容

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        return qs.filter(is_banner=True)


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name','download']
    list_filter = ['course__name', 'name', 'download','add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

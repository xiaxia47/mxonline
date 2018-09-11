# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/10 14:37'

import xadmin

from .models import *


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentAdmin(object):
    list_display = ['user__name', 'course__name', 'comments', 'add_time']
    search_fields = ['user__name', 'course__name', 'comments']
    list_filter = ['user__name', 'course__name', 'comments', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user__name', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__name', 'fav_id', 'fav_type']
    list_filter = ['user__name', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user__name', 'message', 'has_read', 'add_time']
    search_fields = ['user__name', 'message', 'has_read']
    list_filter = ['user__name', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user__name', 'course__name', 'add_time']
    search_fields = ['user__name', 'course__name']
    list_filter = ['user__name', 'course__name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
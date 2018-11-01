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
    list_display = ['user__username', 'course__name', 'comments', 'add_time']
    search_fields = ['user__username', 'course__name', 'comments']
    list_filter = ['user__username', 'course__name', 'comments', 'add_time']

    def user__username(self, object):
        return object.user.username

    def course__name(self, object):
        return object.course.name



class UserFavoriteAdmin(object):
    list_display = ['user__username', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__username', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']

    def user__username(self, object):
        return object.user.username


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user__username', 'course__name', 'add_time']
    search_fields = ['user__username', 'course__name']
    list_filter = ['user__username', 'course__name', 'add_time']

    def user__username(self, object):
        return object.user.username

    def course__name(self, object):
        return object.course.name


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
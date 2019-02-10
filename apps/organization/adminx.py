# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/10 16:35'

import xadmin

from .models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc']


class CourseOrgAdmin(object):
    list_display = ['name', 'click_nums', 'fav_nums', 'address',
                    'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address',
                     'city']
    list_filter = ['name', 'click_nums', 'fav_nums', 'address',
                   'city', 'add_time']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position',
                    'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position',
                     ]
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position',
                   'add_time']
    relfield_style = 'fk-ajax'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

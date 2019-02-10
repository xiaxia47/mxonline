# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2018/9/7 11:47'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner
from xadmin.plugins.auth import UserAdmin

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '教学平台后台管理'
    site_footer = '在线教学平台'
    menu_style = "accordion" #APP伸缩


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o' #修改图标


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
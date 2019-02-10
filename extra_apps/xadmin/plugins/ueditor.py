# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2019/2/10 11:55'
from django.conf import settings

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView, DetailAdminView
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.models import UEditorField


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_settings = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="{}"></script>'.format(
                    settings.STATIC_URL + "ueditor/ueditor.config.js")  # 自己的静态目录
        js += '<script type="text/javascript" src="{}"></script>'.format(
                    settings.STATIC_URL + "ueditor/ueditor.all.min.js")  # 自己的静态目录
        nodes.append(js)


xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, DetailAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)
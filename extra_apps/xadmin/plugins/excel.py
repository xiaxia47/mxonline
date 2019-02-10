# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2019/2/10 14:47'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


class ListImportExcelPlugin(BaseAdminPlugin):
    enable_import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.enable_import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string(template_name='xadmin/excel/model_list.top_toolbar.import.html',
                                             context={}))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
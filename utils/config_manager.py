# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2019/1/6 13:09'
import toml
from MxOnline.settings import CONFIG_ROOT


def load_conf():
    thirdparty_conf = CONFIG_ROOT + '/thirdparty.toml'
    print('loading setting:{}'.format(thirdparty_conf))
    try:
        with open(thirdparty_conf, 'rb') as conf:
            conf_content = conf.read().decode('utf-8')
        conf = toml.loads(conf_content)
    except Exception as e:
        print(e)
        print('load config error')
        conf = None
    return conf


def get_conf_attr(attrs):
    global _conf_instance
    if not _conf_instance:
        _conf_instance = load_conf()
    if isinstance(attrs, list):
        result = {}
        for attr in attrs:
            result[attr] = _conf_instance[attr]
    else:
        result = _conf_instance[attrs]
    return result


_conf_instance = load_conf()
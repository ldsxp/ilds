from djlds.model import *
from djlds.model import get_date_range as get_queryset_date_range


def get_model_fields(modelobj, exclude=None):
    """
    获取数据模型的字段名列表

    :param modelobj: 模型
    :param exclude: 排除
    :return: 返回字段名字列表
    """
    return ModelFields(modelobj, exclude=exclude).field_list


def get_model_name_dict(modelobj, exclude=None):
    """
    获取 model 的 name 字段 和 verbose_name

    :param modelobj: 模型
    :param exclude: 排除
    :return: 键为 name ，值为 verbose_name 的字典
    """
    return ModelFields(modelobj, exclude=exclude).field_dict()

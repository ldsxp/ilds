from collections import OrderedDict

from django.forms.models import model_to_dict  # 获取模型实例的字典
from django.db.models.base import ModelBase, Model
from django.conf import settings
# # from django.db.models import FileField
from django.db.models import Sum

from django.apps import apps
# group_by 这个分组 我喜欢
from django.db.models import Count
from django.db.models import QuerySet
# # from django.db.models import FileField
from django.db.models import Sum

import operator
from functools import reduce
from django.db import models

"""
20181203 添加 搜索多个字段的函数
20181203 ModelFields 添加 获取模型对象
20181203 添加了获取模型的字段，名字和类型的类
20181130 添加 确认是否修改线上数据库（本地操作，因为如果没有修改会直接退出，防止误操作）
20170814 整理了下模型调用
20170814 把模型操作分离出来，以后调用模型都通过这里
20180807 去掉不通用的模型操作，并改成共享库

批量导入例子
loadList = []
kwargs = 需要添加的字段字典
loadList.append(需要添加的库模型(**kwargs))
print('成功导入 %s 行' % len(models_ku.objects.bulk_create(loadList)))
"""


def get_model(value, model_dict=None, is_exact=True) -> Model:
    """
    通过库的名字或模型的名字获取模型

    例子：
        ku_model = get_model('酷狗', model_dict=None, is_exact=True)
        if not ku_model:
            raise RuntimeError('没有找到模型！')

    :param value: 要获取的模型，如果本身就是模型，直接返回
    :param ku_dict: 从模型字典（模型名字：模型）中获取模型
    :param is_exact: 精确模式，控制是否匹配文件名中包含模型名的情况
    :return: Model
    """

    if isinstance(value, ModelBase):
        return value

    _model_dict = {app.__name__: app for app in apps.get_models() if
                   'django.contrib.' not in str(app) and '.models.' in str(app)}
    # print(_model_dict)

    # 检查模型的名称
    if value in _model_dict:
        return _model_dict[value]
    elif model_dict is not None:
        if is_exact:
            # 如果是精确模式，匹配以后就可以返回
            if value in model_dict:
                return model_dict[value]
        else:
            # 不是精确模式，主要是处理文件名中包含模型名字的情况
            for ku_name in model_dict.keys():
                # print(ku_name)
                if ku_name in value:
                    return model_dict[ku_name]


def get_search_results(queryset, search_fields, search_term):
    """
    搜索，返回包含查询集的
    来自：from django.contrib.admin.options import ModelAdmin
    """

    # 应用关键字搜索。
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    if search_fields and search_term:
        orm_lookups = [construct_search(str(search_field))
                       for search_field in search_fields]
        for bit in search_term.split():
            or_queries = [models.Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            #
            queryset = queryset.filter(reduce(operator.or_, or_queries))

    return queryset


class ModelFields():
    """
    获取模型的字段，名字和类型。
    可以用来替代：
        get_model_verbose_name_dict
        get_model_name_dict
        get_model_verbose_names
        get_model_verbose_namesget_model_fields
        get_model_fields

    例子：
    from ilds.django.model import ModelFields
    print(ModelFields(mymodel).verbose_to_type('标题'))
    for i in ModelFields(mymodel).iter('type'):
    print(i)
    """

    def __init__(self, model, exclude=None):
        """
        初始化
        """
        self.field_list = []
        self.verbose_list = []
        self.type_list = []
        self.fields = []

        if exclude is None:
            exclude = []
        for f in model._meta.fields:  # model._meta._get_fields(reverse=False) 包括 ManyToMany 字段
            field_name = f.name
            verbose_name = f.verbose_name
            type_name = type(f).__name__
            if field_name in exclude or verbose_name in exclude or type_name in exclude:
                continue
            self.field_list.append(field_name)
            self.verbose_list.append(verbose_name)
            self.type_list.append(type_name)
            self.fields.append(f)

        self.count = len(self.field_list)
        # print(self.field_list)
        # print(self.verbose_list)
        # print(self.type_list)

    def field_to_verbose(self, field):
        """通过 field_name 获取 verbose_name"""
        if field in self.field_list:
            return self.verbose_list[self.field_list.index(field)]

    def field_to_type(self, field):
        """通过 field_name 获取 type_name"""
        if field in self.field_list:
            return self.type_list[self.field_list.index(field)]

    def verbose_to_field(self, field):
        """通过 verbose_name 获取 field_name"""
        if field in self.verbose_list:
            return self.field_list[self.verbose_list.index(field)]

    def verbose_to_type(self, field):
        """通过 verbose_name 获取 type_name"""
        if field in self.verbose_list:
            return self.type_list[self.verbose_list.index(field)]

    def get_field(self, name):
        """通过 名字获取 field 属性
        按 field_name -> verbose_name 的顺序查找，
        已经找到就不在继续查找，没有找到返回空
        """
        if name in self.field_list:
            return self.fields[self.field_list.index(name)]
        elif name in self.verbose_list:
            return self.fields[self.verbose_list.index(name)]

    def iter(self, *args):
        """获取指定字段的生成器"""
        iter_dict = {
            'field': self.field_list,
            'verbose': self.verbose_list,
            'type': self.type_list,
        }
        if not args:
            args = ['field']
        else:
            if [arg for arg in args if arg not in iter_dict]:
                raise ValueError(f"参数错误：{args}，可用参数为：'field', 'verbose', 'type'")

        # print([iter_dict[arg][1] for arg in args])
        # print([i for i in range(self.count)])
        return ([iter_dict[arg][i] for arg in args] for i in range(self.count))


# 从上面改成输入 模型 和 排除
def get_model_verbose_name_dict(modelobj, exclude=None):
    """
    获取 model 的 verbose_name 和 name 的字段

    :param modelobj: 模型
    :param exclude: 排除
    :return: 键为 verbose_name，值为 name 的字典
    """

    filed = modelobj._meta.fields
    # print(filed)

    if exclude is None:
        params = [f for f in filed]
    else:
        params = [f for f in filed if f.name not in exclude]

    field_dict = OrderedDict()
    for i in params:
        field_dict[i.verbose_name] = i.name

    return field_dict


def get_model_name_dict(modelobj, exclude=None):
    """
    获取 model 的 name 字段 和 verbose_name

    :param modelobj: 模型
    :param exclude: 排除
    :return: 键为 name ，值为 verbose_name 的字典
    """

    filed = modelobj._meta.fields
    # print(filed)

    if exclude is None:
        params = [f for f in filed]
    else:
        params = [f for f in filed if f.name not in exclude]

    field_dict = OrderedDict()
    for i in params:
        field_dict[i.name] = i.verbose_name

    return field_dict


def get_model_verbose_names(modelobj, exclude=None):
    """
    获取数据模型的 verbose_name 名字列表

    :param modelobj: 模型
    :param exclude: 排除
    :return: 返回 verbose_name 列表
    """
    if exclude is None:
        exclude = []
    return [f.verbose_name for f in modelobj._meta.fields if f.name not in exclude]


def get_model_fields(modelobj, exclude=None):
    """
    获取数据模型的字段名列表

    :param modelobj: 模型
    :param exclude: 排除
    :return: 返回字段名字列表
    """
    if exclude is None:
        exclude = []
    return [f.name for f in modelobj._meta.fields if f.name not in exclude]


def get_fieldfile_path(_fieldfile):
    """
    获取 模型 FileField 路径
    """
    # print(_fieldfile.path)
    # print(_fieldfile.upfile.name)
    # print(_fieldfile.read())
    try:
        return _fieldfile.path
    except:
        return None


# def model_to_dict2(model_queryset, exclude):
#     model_dict = model_to_dict(model_queryset, exclude=exclude)

def get_queryset_sum(queryset, field_list, *args):
    """
    计算 QuerySet 的和 参数 QuerySet 需要求和的字段  需要显示的字段
    """

    kwargs = {}

    try:
        # 获取需要求和的内容
        for i in field_list:
            # print(i)
            if '_quanli_' in i:
                # print('_quanli_')
                continue
            elif i.endswith('_int') or i.endswith('_float'):
                if 'rmb_int' in i:
                    pass
                elif 'fencheng_int' in i:
                    pass
                else:
                    # print(i)
                    kwargs[i] = Sum(i)
        if kwargs:
            return queryset.values(*args).annotate(**kwargs)
        else:
            return None
    except:
        pass
    return None


def group_by(query_set, group_by):
    """
    util:django 获取分类列表 ( 对某些取到的QuerySet分组)

    例如获取厂牌名称
    print(group_by(objs,'shouquan_changpai'))
    》 ['厂牌名称1', '厂牌名称2', ...]

    :param query_set:
    :param group_by: 需要分组的字段
    :return: 分组字段的内容列表
    """

    assert isinstance(query_set, QuerySet)
    django_groups = query_set.values(group_by).annotate(Count(group_by))
    groups = []
    for dict_ in django_groups:
        # print(dict_)
        groups.append(dict_.get(group_by))
    return groups


def get_queryset_date_range(queryset, date_field='shujuriqi_date'):
    """
    获取 QuerySet 的日期间隔 参数 queryset，日期的字段
    """

    fromdate = queryset.order_by(date_field)[:1].values_list(date_field)[0][0].strftime("%Y-%m-%d")
    todate = queryset.order_by('-' + date_field)[:1].values_list(date_field)[0][0].strftime("%Y-%m-%d")
    return fromdate, todate


def confirm_db():
    """
    确认是否修改线上数据库
    本地操作，因为如果没有修改会直接退出，防止误操作
    """
    import wx
    app = wx.App()
    if not settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        dlg = wx.MessageDialog(None, "正在修改服务器数据库，是否继续？", "警告：不是连接的本地数据库", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            print("修改服务器数据库......")
        else:
            exit()


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_model)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=ModelFields)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_model_verbose_name_dict)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_model_name_dict)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_model_verbose_names)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_model_fields)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_fieldfile_path)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_queryset_sum)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=group_by)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_queryset_date_range)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=confirm_db)

    print(doc_text)


if __name__ == "__main__":
    from time import time

    t1 = time()

    doc()

    print('用时 %.2f 秒' % (time() - t1))

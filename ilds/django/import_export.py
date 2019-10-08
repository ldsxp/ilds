# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：import_export.py
#   版本：0.1
#   作者：lds
#   日期：2019-05-05
#   语言：Python 3.X
#   说明：django 导入和导出
# ---------------------------------------

import csv

# 获取模型实例的字典
from django.forms.models import model_to_dict

from ilds.django.model import get_model_verbose_names
from ilds.django.model import get_model_verbose_name_dict as get_model_field
from ilds.django.model import get_fieldfile_path as get_model_fieldfile_path


class ModelData():
    """
    根据 django 模型转换导入数据
    """

    # 获取字段类型，处理一部分类型
    WIDGETS_MAP = {
        # 'ManyToManyField': 'get_m2m_widget',
        # 'OneToOneField': 'get_fk_widget',
        # 'ForeignKey': 'get_fk_widget',
        # 'DecimalField': widgets.DecimalWidget,
        # 'DateTimeField': widgets.DateTimeWidget,
        # 'DateField': widgets.DateWidget,
        # 'TimeField': widgets.TimeWidget,
        # 'DurationField': widgets.DurationWidget,
        # 'FloatField': float,
        # 'IntegerField': widgets.IntegerWidget,
        # 'PositiveIntegerField': widgets.IntegerWidget,
        # 'BigIntegerField': widgets.IntegerWidget,
        # 'PositiveSmallIntegerField': widgets.IntegerWidget,
        # 'SmallIntegerField': widgets.IntegerWidget,
        # 'AutoField': widgets.IntegerWidget,
        # 'NullBooleanField': widgets.BooleanWidget,
        # 'BooleanField': widgets.BooleanWidget,
    }

    def __init__(self, model, row, import_names=None, exclude=None):

        # 需要转换的 id 然后批量转换
        # 如果有需要 再添加

        # print(filed)

        if exclude is None:
            exclude = []

        self.import_fields = []
        self.import_index = []
        self.zhuanhuan = {}

        names = {}
        verbose_names = {}
        if import_names is None:
            import_names = {}

        for f in model._meta.fields:
            # print('处理不同字段内容', isinstance(f, models.BooleanField))
            # print('获取模型的字段名', f.get_internal_type())
            internal_type = f.get_internal_type() if callable(getattr(f, "get_internal_type", None)) else ""
            # print(internal_type, f.verbose_name, f.name)
            names[f.name] = {'name': f.name, 'internal_type': internal_type}
            verbose_names[f.verbose_name] = {'name': f.name, 'internal_type': internal_type}

        for i, field in enumerate(row):
            # 排除的内容
            if field in exclude:
                continue

            # 重命名的内容
            if field in import_names:
                field = import_names[field]

            # 字段名导入
            if field in names:
                self.import_fields.append(names[field]['name'])
                self.import_index.append(i)
                if names[field]['internal_type'] in self.WIDGETS_MAP:
                    self.zhuanhuan[names[field]['name']] = self.WIDGETS_MAP[names[field]['internal_type']]
            # 按名字导入
            elif field in verbose_names:
                self.import_fields.append(verbose_names[field]['name'])
                self.import_index.append(i)
                if verbose_names[field]['internal_type'] in self.WIDGETS_MAP:
                    self.zhuanhuan[verbose_names[field]['name']] = self.WIDGETS_MAP[
                        verbose_names[field]['internal_type']]
            # 没有导入的内容
            else:
                # pass
                # print('导入失败：-------------------表头 %s %s 应该为 %s 。-------------------' % (i + 1, field, now_0[i]))
                raise RuntimeError('导入失败：row[%s]：%s 不能导入数据库。' % (i + 1, field))

    def get_import_data(self, row):
        """
        """
        import_data = {}

        for i in range(len(self.import_index)):
            field = self.import_fields[i]
            index = self.import_index[i]
            val = row[index]
            if not val:
                continue
            if field in self.zhuanhuan:
                # print('转换类型', self.zhuanhuan[field], val)
                val = self.zhuanhuan[field](val)

            import_data[field] = val

        return import_data


def dj_import_csv(ku_model, csv_file):
    """
    导入csv文件到数据库

    注意：需要处理日期和文件名的不要用她导入，她只用于备份和恢复。
    """

    print('导入开始 ---------------------------------------------------------\n', csv_file)

    # 读取csv文件
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            loadList = []
            iter_reader = iter(reader)
            export = ModelData(ku_model, next(iter_reader))
            for row in iter_reader:
                # print(ku_field, xls_row, row)
                kwargs = export.get_import_data(row)
                # print(kwargs)
                loadList.append(ku_model(**kwargs))
        except csv.Error as e:
            return (f'file {csv_file}, line {reader.line_num}: {e}')
        else:
            info = '成功导入 %s 行' % len(ku_model.objects.bulk_create(loadList))
            print(info)
            print('---------------------------------------------------------')
            return info


class LdsExportCsv():
    """
    写入数据到 csv 文件
    支持自定义写入的表头和要导出的字段

    例子
    from ilds.django.model import get_model_verbose_names

    # ku_model = 要导出的模型
    objs = ku_model.objects.all()
    # 找到的歌曲列表
    if objs.exists():
        xlsxfile = r'导出：测试.csv'
        ex_csv = LdsExportCsv(ku_model, xlsxfile)  # 歌曲库的中文名
        ex_csv.set_title_field(*get_model_verbose_names(ku_model))
        # 或者元组列表
        # ex_csv.set_title_field('歌曲名称', '表演者', '专辑名称', ) # , row=3, col=3
        for obj in objs:
            ex_csv.append(obj)
        info = ex_csv.print_count_info()
        ex_csv.close()
    else:
        print('没有找到歌曲')
    """

    def __init__(self, ku_model, work_file):
        """初始化"""
        self.title = []
        self.export = None

        # 要处理的库
        self.ku_model = ku_model

        # 写入csv文件
        self.csvfile = open(work_file, 'w', newline='', encoding='utf-8')  # 有软件打开乱码
        self.writer_csv = csv.writer(self.csvfile)

        self.gequ_dict = {}

        # 设置排除内容
        self.exclude = ['denglushijian_date']  # 'id',

        # 初始化统计
        self.count_all = 0
        self.tongji_info = {}
        self.count_merge = 0

    def set_title_field(self, *export):
        """
        设置标题和写入的内容
        export 是要导出列的名字列表
        """

        # 需要获取数据的字段列表
        self.field_list = []
        self.export = export

        # 获取模型的字段
        model_field = get_model_field(self.ku_model, self.exclude)
        # pprint(model_field)

        # 写表头
        csv_row = []
        for i_export in self.export:
            i_export = i_export.strip()
            if i_export:
                try:
                    self.field_list.append(model_field[i_export])
                except:
                    self.field_list.append('None')
                # print(self.field_list)
                csv_row.append(i_export)
        self.writer_csv.writerow(csv_row)

        self.init_count()

        return

    def append(self, date, row=0, col=0):
        """
        写入 csv 文件
        date 要写入的数据
        """

        model_dict = model_to_dict(date, exclude=self.exclude)

        # 写入文件
        # print(model_dict)
        # print(self.field_list)
        csv_row = []
        for i_field_list in self.field_list:
            try:
                # 统计信息
                if i_field_list in self.tongji_info:
                    value = model_dict[i_field_list]
                    if i_field_list.endswith('_float'):
                        self.tongji_info[i_field_list] += float(value)
                    else:
                        self.tongji_info[i_field_list] += int(value)
                    # print(self.tongji_info)
                # 处理日期
                if i_field_list == 'shujuriqi_date':
                    value = model_dict[i_field_list].strftime("%Y-%m")
                elif i_field_list.endswith('_date'):
                    value = model_dict[i_field_list].strftime("%Y-%m-%d")
                # 处理文件
                elif i_field_list.endswith('_file'):
                    value = get_model_fieldfile_path(model_dict[i_field_list])
                else:
                    value = model_dict[i_field_list]
            except:
                value = ''
            csv_row.append(value)
        self.writer_csv.writerow(csv_row)

        # print(model_dict)
        self.count_all += 1
        return

    def get_count_list(self):
        """获取统计信息的列表 列表内容是字典 键为 count_name count_field count"""
        count_list = []
        model_fields = get_model_field(self.ku_model)
        # print(model_fields)
        if self.tongji_info:
            for k, v in model_fields.items():
                _dict = {}
                _field = self.tongji_info.get(v)
                # print(k,v,_field)
                if not _field is None:
                    _dict['count_name'] = k
                    _dict['count_field'] = v
                    _dict['count'] = self.tongji_info[v]
                    count_list.append(_dict)
        return count_list

    def print_count_info(self):
        """打印统计信息"""
        print_info = '导出：%s    总共：%s' % (self.count_all - self.count_merge, self.count_all)
        for _count in self.get_count_list():
            print_info += '%s：%s    ' % (_count['count_name'], _count['count'])  # _count['count_field']
        print(print_info)
        return print_info

    def init_count(self):
        """ 初始化需要统计的内容"""

        self.tongji_info = {}
        # print(field_list)
        for i in self.field_list:
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
                    self.tongji_info[i] = 0

        # print(self.tongji_info)

    def close(self):
        """
        写入结束，关闭文件
        """
        self.csvfile.close()

    def __repr__(self):
        return str(self.export)


def dj_export_csv(ku_model, sep=''):
    """
    导出数据为csv文件
    """

    name_str = '导出 %s' % ku_model.__name__
    # name_str = '导出 %s(%s)' % (ku_str, ku.__name__)

    EXPOET_EAX = 1000000  #
    data_list = ku_model.objects.all()
    # 自定义了到处方式
    # # 按日期导出
    # kwargs = {}
    # kwargs['shujuriqi_date__range'] = ['2018-01-01', '2100-01-01']
    # data_list = ku.objects.filter(**kwargs)
    try:
        data_count = data_list.count()
    except Exception as e:
        return (ku_model.__name__, '没有歌曲导出 ', e)

    # 找到的歌曲列表
    if data_count:
        print('---------------------------------------------------------')
        print('开始 %s' % name_str)
        print()

        print('搜索结果：', data_count)
        if data_count > EXPOET_EAX:
            export_start = 0
            export_stop = EXPOET_EAX
            info = '已分多个文件导出：'
            # print(info)
            while True:
                if export_start > data_count:
                    break
                data_list = ku_model.objects.all()[export_start:export_stop]
                if export_stop == EXPOET_EAX:
                    name = name_str + '.csv'
                else:
                    # print(type(export_start),type(EXPOET_EAX),type(export_start/EXPOET_EAX))
                    name = name_str + '_%03d.csv' % int(export_start / EXPOET_EAX)
                mycsv = LdsExportCsv(ku_model, name)  # 歌曲库的中文名
                mycsv.set_title_field(*get_model_verbose_names(ku_model, exclude=['id', 'denglushijian_date',
                                                                                  'xiugaizhe']))  # , row=3, col=3
                for i_data_list in data_list:
                    # print(i_data_list)
                    mycsv.append(i_data_list)
                info += sep + mycsv.print_count_info()
                mycsv.close()
                export_start += EXPOET_EAX
                export_stop += EXPOET_EAX
        else:
            print('没有超过 %s' % EXPOET_EAX)
            mycsv = LdsExportCsv(ku_model, name_str + '.csv')  # 歌曲库的中文名
            mycsv.set_title_field(
                *get_model_verbose_names(ku_model, exclude=['id', 'denglushijian_date', 'xiugaizhe']))  # , row=3, col=3
            for i_data_list in data_list:
                # print(i_data_list)
                mycsv.append(i_data_list)
            mycsv.close()
            info = mycsv.print_count_info()
            # print(mycsv.tongji_info)
            # mycsv.print_count_info()
            print()
            print('导出结束')
            print('---------------------------------------------------------')
    else:
        info = (ku_model.__name__, '库没有歌曲')

    # print(info)
    return info


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=ModelData)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=dj_import_csv)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=LdsExportCsv)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=dj_export_csv)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

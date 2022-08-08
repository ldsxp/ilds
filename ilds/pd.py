# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：pd.py
#   版本：0.4
#   作者：lds
#   日期：2021-09-30
#   语言：Python 3.X
#   说明：pandas 常用的函数集合，TODO 添加一些小抄在这里！
# ---------------------------------------
import os
from pathlib import Path
from collections import OrderedDict

from colorama import Fore, Back, Style

from ilds.file import get_dir_files

try:
    import pandas as pd
except ImportError as e:
    print(Fore.RED + "注：导入 pandas 失败，请安装它: pip install pandas", Style.RESET_ALL)
    pass


def get_columns_index(df, columns):
    """获取列名称在 DataFrame 中的索引"""
    if isinstance(columns, str):
        columns = [columns]
    columns_index = []
    for col in columns:
        columns_index.append(df.columns.get_loc(col))
    # print('columns_index', columns_index)
    return columns_index


def get_df_list(file, concat_columns=None, add_source_column=True, is_print=True):
    df_list = []
    with pd.ExcelFile(file) as excel:
        sheet_names = excel.sheet_names
        if is_print:
            print('表薄名称列表：', sheet_names)
        # 通过表薄名字读取表单
        # data['总表'] = pd.read_excel(excel, sheet_name='总表')
        # 读取全部表
        for sheet_name in sheet_names:
            _df = pd.read_excel(excel, sheet_name=sheet_name, header=0)
            # _df = pd.read_excel(excel, sheet_name=0, header=0)
            if is_print:
                print('表薄名称：', sheet_name, '\t', '行数：', len(_df), '\t', '文件：', file)
            # if 'Metadatas' != sheet_name:
            #     print('跳过内容', sheet_name)
            #     continue
            if add_source_column:
                _df['本行来自'] = f"{os.path.split(file)[1]} - {sheet_name}"
            # 是否指定要合并的列
            if concat_columns is not None:
                _df = _df[concat_columns]
            df_list.append(_df)
    return df_list


def get_excel_data(file, columns=None, add_source_column=True, only_read_first_table=False, is_print=True):
    """
    读取 Excel 数据

    返回数据：'file_name', 'index', 'sheet_name', 'sheet_names', 'count', 'columns', 'df'

    :param file: Excel 文件
    :param columns: 指定要读取的列，我们会只读取这些数据，方便用来合并
    :param add_source_column: 添加内容来源
    :param only_read_first_table: 只读取第一个表格
    :param is_print: 打印读取信息
    :return: {'file_name', 'index', 'sheet_name', 'sheet_names', 'count', 'columns', 'df'}
    """
    data = OrderedDict()

    with pd.ExcelFile(file) as excel:
        sheet_names = excel.sheet_names
        if is_print:
            print('表薄名称列表：', sheet_names)
        # 通过表薄名字读取表单
        # data['总表'] = pd.read_excel(excel, sheet_name='总表')
        # 读取全部表
        for index, sheet_name in enumerate(sheet_names):
            _df = pd.read_excel(excel, sheet_name=sheet_name, header=0)
            file_name = os.path.basename(file)
            count = len(_df)

            if is_print:
                print('表薄名称：', sheet_name, '\t', '行数：', count, '\t', '文件：', file)

            if add_source_column:
                _df['本行来自'] = f"{file_name} - {sheet_name}"

            # 是否指定要合并的列
            if columns is not None:
                _df = _df[columns]

            df_data = {
                'file_name': file_name,
                'index': index,
                'sheet_name': sheet_name,
                'sheet_names': sheet_names,
                'count': count,
                'columns': list(_df.columns),
                'df': _df,
            }

            if only_read_first_table:
                data = df_data
                break

            data[sheet_name] = df_data

    return data


def merging_excel_sheet(file, concat_columns=None, add_source_column=True, is_print=True, **concat_kwargs):
    """
    合并 Excel 表薄内容

    :param file: 要合并文件的路径
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :return:
    """

    df_list = get_df_list(file, concat_columns, add_source_column, is_print)
    count = sum([len(df) for df in df_list])
    df = pd.concat(df_list, **concat_kwargs)  # result
    print('合并数据行数：', len(df), '导入数据行数统计：', count)
    return df


def merging_excel_file_data(file_dir, ext='', concat_columns=None, add_source_column=True, is_print=True,
                            **concat_kwargs):
    """
    合并多个 Excel 文件内容

    :param file_dir: 合并文件的路径
    :param ext: 要合并的文件后缀名，默认是文件夹中的全部文件
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :param is_print: 打印信息
    :return:
    """
    all_len = 0
    frames = []
    for file in get_dir_files(file_dir, ext):
        if is_print:
            print(file)
        df_list = get_df_list(file, concat_columns, add_source_column, is_print)
        all_len += sum([len(df) for df in df_list])
        frames.extend(df_list)

    _df = pd.concat(frames, **concat_kwargs)  # result
    if is_print:
        print('合并数据行数：', len(_df), '原始数据行数：', all_len)
    return _df


def split_excel_sheet(file, dst_dir=None):
    """
    拆分 Excel 表薄内容

    :param file: 要拆分的文件
    :param dst_dir: 拆分文件的保存目录
    :return:
    """
    file = Path(file)

    if dst_dir is None:
        dst_dir = file.parent

    excel_data = get_excel_data(file, columns=None, add_source_column=False, only_read_first_table=False,
                                is_print=False)
    print('sheet_names', list(excel_data.keys()))

    for sheet_name, d in excel_data.items():
        df = d['df']
        to_file = dst_dir / f"{file.stem}-{d['sheet_name']}{file.suffix}"
        print(f"保存表薄: {d['sheet_name']}, 行数: {d['count']}", to_file)
        with pd.ExcelWriter(to_file) as writer:
            df.to_excel(writer, sheet_name=d['sheet_name'])


def writer_excel(obj, path, index=False, use_zip64=False):
    """
    保存 Excel 文件

    :param obj:
    :param path:
    :param index: 是否添加索引
    :param use_zip64:
    :return:
    """
    if isinstance(obj, dict):
        with pd.ExcelWriter(path) as writer:
            for sheet_name, df_data in obj.items():
                df_data.to_excel(writer, sheet_name=sheet_name, index=index)
            if use_zip64:
                writer.book.use_zip64()
    else:
        with pd.ExcelWriter(path) as writer:
            obj.to_excel(writer, sheet_name='Sheet1', index=index)
            if use_zip64:
                writer.book.use_zip64()


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_columns_index)
    # doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：pd.py
#   版本：0.6
#   作者：lds
#   日期：2023-04-27
#   语言：Python 3.X
#   说明：pandas 常用的函数集合，TODO 添加一些小抄在这里！
# ---------------------------------------
import os
from pathlib import Path
from collections import OrderedDict

from colorama import Fore, Back, Style

from ilds.file import get_dir_files
from openpyxl import load_workbook

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


def get_df_list(file, sheet_names=None, concat_columns=None, add_source_column=True, strict_mode=False, is_print=True):
    df_list = []

    with pd.ExcelFile(file) as excel:
        if sheet_names is None:
            sheet_names = excel.sheet_names
        else:
            # 确保Excel文件中提供的 sheet_names 存在
            invalid_sheets = set(sheet_names) - set(excel.sheet_names)
            if invalid_sheets:
                raise ValueError(f"Excel 文件中不存在以下标题：{invalid_sheets}")

            # 当严格模式开启时，检查是否有额外的表薄名称在文件中
            if strict_mode:
                extra_sheets = set(excel.sheet_names) - set(sheet_names)
                if extra_sheets:
                    raise ValueError(f"Excel 文件中包含了未在“{sheet_names}”中的额外标题：{extra_sheets}")

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


def get_excel_data(file, columns=None, add_source_column=True, only_read_first_table=False, read_sheet_state=False,
                   is_print=True):
    """
    读取 Excel 数据

    返回数据：'file_name', 'index', 'sheet_name', 'sheet_names', 'count', 'columns', 'df'

    :param file: Excel 文件
    :param columns: 指定要读取的列，我们会只读取这些数据，方便用来合并
    :param add_source_column: 添加内容来源
    :param only_read_first_table: 只读取第一个表格
    :param read_sheet_state: 读取表格的状态，这样就可以处理隐藏表格
    :param is_print: 打印读取信息
    :return: {'file_name', 'index', 'sheet_name', 'sheet_names', 'count', 'columns', 'df'}
    """
    data = OrderedDict()

    if read_sheet_state:
        try:
            wb = load_workbook(file, read_only=False)
            sheet_state_data = {name: wb[name].sheet_state for name in wb.sheetnames}
            # print(sheet_state_data)
            wb.close()
        except Exception as e:
            print('get_excel_data 读取表格状态失败', e)
            sheet_state_data = {}
    else:
        sheet_state_data = {}

    with pd.ExcelFile(file) as excel:
        sheet_names = excel.sheet_names
        if is_print:
            print('表薄名称列表：', sheet_names)
        # 通过表薄名字读取表单
        # data['总表'] = pd.read_excel(excel, sheet_name='总表')
        # 读取全部表
        for index, sheet_name in enumerate(sheet_names):
            sheet_state = sheet_state_data.get(sheet_name, None)
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
                'sheet_state': sheet_state,
                'count': count,
                'columns': list(_df.columns),
                'df': _df,
            }

            if only_read_first_table:
                data = df_data
                break

            data[sheet_name] = df_data

    return data


def merging_excel_sheet(file, sheet_names=None, concat_columns=None, add_source_column=True, strict_mode=False, is_print=True, **concat_kwargs):
    """
    合并 Excel 表薄内容

    :param file: 要合并文件的路径
    :param sheet_names: 要合并的表
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :param strict_mode: 添加一个严格模式的参数，限制要合并文件的标题
    :param is_print: 打印信息
    :return:
    """
    df_list = get_df_list(file=file, sheet_names=sheet_names, concat_columns=concat_columns, add_source_column=add_source_column, strict_mode=strict_mode,
                          is_print=is_print)
    count = sum([len(df) for df in df_list])
    df = pd.concat(df_list, **concat_kwargs)  # result
    print('合并数据行数：', len(df), '导入数据行数统计：', count)
    return df


def merging_excel_file_data(file_dir_or_file_list, ext='', sheet_names=None, concat_columns=None, add_source_column=True, is_print=True,
                            **concat_kwargs):
    """
    合并多个 Excel 文件内容

    :param file_dir_or_file_list: 合并文件的路径或者文件列表
    :param ext: 要合并的文件后缀名，默认是文件夹中的全部文件
    :param sheet_names: 要合并的表
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :param is_print: 打印信息
    :return:
    """
    all_len = 0
    frames = []

    if isinstance(file_dir_or_file_list, list):
        file_list = file_dir_or_file_list
    else:
        file_list = get_dir_files(file_dir_or_file_list, ext)

    for file in file_list:
        if is_print:
            print('处理文件:', file)
        df_list = get_df_list(file, sheet_names, concat_columns, add_source_column, is_print)
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
        dst_dir = file.parent / f'{file.stem} - 拆分'
    elif isinstance(dst_dir, str):
        dst_dir = Path(dst_dir)

    if not dst_dir.exists():
        dst_dir.mkdir()

    xlsx = pd.ExcelFile(file)
    sheet_names = xlsx.sheet_names
    print('sheet_names', sheet_names)

    for sheet_name in sheet_names:
        df = xlsx.parse(sheet_name)
        to_file = dst_dir / f"{sheet_name}{file.suffix}"
        print(f"保存表薄: {sheet_name}, 文件: {to_file}")
        with pd.ExcelWriter(to_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"拆分完成，拆分文件保存在 '{dst_dir}' 文件夹中。")


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

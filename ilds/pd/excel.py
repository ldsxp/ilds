import os
from pathlib import Path

import pandas as pd
from ilds.file import get_dir_files
from ilds.pd.read import get_df_list


def merging_excel_sheet(file, sheet_names=None, concat_columns=None, add_source_column=True, strict_mode=False, exclude_sheets=None, is_print=True, **concat_kwargs):
    """
    合并 Excel 表薄内容

    :param file: 要合并文件的路径
    :param sheet_names: 要合并的表
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :param strict_mode: 添加一个严格模式的参数，限制要合并文件的标题
    :param exclude_sheets: 合并的时候要排除的表薄
    :param is_print: 打印信息
    :return:
    """
    df_list = get_df_list(file=file, sheet_names=sheet_names, concat_columns=concat_columns, add_source_column=add_source_column, strict_mode=strict_mode,
                          exclude_sheets=exclude_sheets, is_print=is_print)
    count = sum([len(df) for df in df_list])
    df = pd.concat(df_list, **concat_kwargs)  # result
    print('合并数据行数：', len(df), '导入数据行数统计：', count)
    return df


def merging_excel_file_data(file_dir_or_file_list, ext='', sheet_names=None, concat_columns=None, add_source_column=True, strict_mode=False, exclude_sheets=None,
                            is_print=True, **concat_kwargs):
    """
    合并多个 Excel 文件内容

    :param file_dir_or_file_list: 合并文件的路径或者文件列表
    :param ext: 要合并的文件后缀名，默认是文件夹中的全部文件
    :param sheet_names: 要合并的表
    :param concat_columns: 指定要合并的列名列表
    :param add_source_column: 是否添加原始来源
    :param strict_mode: 添加一个严格模式的参数，限制要合并文件的标题
    :param exclude_sheets: 合并的时候要排除的表薄
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
        df_list = get_df_list(file=file, sheet_names=sheet_names, concat_columns=concat_columns, add_source_column=add_source_column, strict_mode=strict_mode,
                              exclude_sheets=exclude_sheets, is_print=is_print)
        all_len += sum([len(df) for df in df_list])
        frames.extend(df_list)
    if frames:
        _df = pd.concat(frames, **concat_kwargs)  # result
    else:
        _df = pd.DataFrame()
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
    dst_dir = Path(dst_dir or (file.parent / f'{file.stem} - 拆分'))
    dst_dir.mkdir(exist_ok=True)

    with pd.ExcelFile(file) as xlsx:
        for sheet_name in xlsx.sheet_names:
            df = xlsx.parse(sheet_name)
            to_file = dst_dir / f"{sheet_name},{file.suffix}"
            print(f"保存表: {sheet_name}, 文件: {to_file}")
            with pd.ExcelWriter(to_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"拆分完成，拆分文件保存在 '{dst_dir}' 文件夹中。")


def save_to_multiple_excel_files(df, filename_prefix, write_function, max_rows=1048576 - 2):
    """
    把 DataFrame 数据安全保存到 Excel
    在超过 Excel 最大行数的时候，保存为多个文件

    将 DataFrame 数据安全保存到 Excel 文件中

    此函数检查 DataFrame 的行数，如果行数超过 Excel 的最大限制，则将数据拆分为多个文件保存

    参数：
    - df: pandas.DataFrame
        要保存的数据。
    - filename_prefix: str
        用于生成文件名的前缀
    - write_function: callable
        实际执行写入 Excel 文件操作的函数，应接受 (df, filename) 作为参数
    - max_rows: int, 可选
        每个 Excel 文件中允许的最大行数，默认为 Excel 限制的 1048576 减去 2 行
    """
    save_files = []

    if str(filename_prefix).endswith('.xlsx'):
        filename_prefix = str(filename_prefix)[:-5]

    total_rows = len(df)

    if total_rows <= max_rows:
        # 数据行数小于或等于最大限制，使用原始文件名
        filename = f"{filename_prefix}.xlsx"
        write_function(df, filename)
        save_files.append(filename)
    else:
        # 数据行数大于最大限制，分块并增加索引后缀
        file_idx = 1
        for start_row in range(0, total_rows, max_rows):
            end_row = min(start_row + max_rows, total_rows)
            sub_df = df.iloc[start_row:end_row]

            filename = f"{filename_prefix}_{file_idx}.xlsx"
            write_function(sub_df, filename)
            save_files.append(filename)
            file_idx += 1

    return save_files

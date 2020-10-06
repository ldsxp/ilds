# ---------------------------------------
#   程序：everything.py
#   版本：0.1
#   作者：lds
#   日期：2020-10-06
#   语言：Python 3.X
#   说明：Everything 搜索相关的函数集合

import os
import sys
import re
import csv
import datetime
from time import time, sleep
import shutil

from ilds.excel_xlrd import ReadXlsx, get_gequ_geshou_line
from ilds.file import human_size

# everything 文件列表
# https://www.voidtools.com/zh-cn/support/everything/file_lists/

"""
EFU 文件列表是什么格式？

EFU 文件是包含文件名、大小、日期以及属性列表的逗号分隔值 (CSV) 文件。
指定至少文件名分栏时需要标头。
文件大小指定为字节。
日期是十进制 FILETIMEs (1601 年 1 月 1 日 100-纳秒) 或 ISO 8601 格式日期。
属性可以为 0 或多个 Windows 文件属性。
EFU 文件是 UTF-8 编码。
"""


def reader_efu(efu_file, encoding='utf-8'):
    """
    读取 EFU 文件

    文件是包含文件名、大小、日期以及属性列表的逗号分隔值 (CSV) 文件

    header ['Filename', 'Size', 'Date Modified', 'Date Created', 'Attributes']
    """
    rows = []
    # 读取csv文件
    with open(efu_file, newline='', encoding=encoding) as f:
        reader = csv.reader(f)  # delimiter=':', quoting=csv.QUOTE_NONE

        iter_reader = iter(reader)
        header = next(iter_reader)  # fieldnames
        # print(header)
        rows.append(header)

        try:
            for row in iter_reader:
                # print(row)
                rows.append(row)
        except csv.Error as e:
            print(f'csv.Error file {efu_file}, line {reader.line_num}: {e}')
            return
        # else:
        #     print('读取完成')
    return rows


def writer_efu(efu_file, rows, encoding='utf-8'):
    """
    写入 EFU 文件

    文件是包含文件名、大小、日期以及属性列表的逗号分隔值 (CSV) 文件
    """
    # 写入csv文件
    with open(efu_file, 'w', newline='', encoding=encoding) as f:
        writer = csv.writer(f)
        # 写入单行
        # writer.writerow(row)
        # 写入多行
        writer.writerows(rows)


def get_efu_data(file_dir, str_time='%Y-%m-%d %H:%M:%S'):
    data = []
    yield ['Filename', 'Size', 'Date Modified', 'Date Created', 'Attributes']
    from ilds.file import get_walk_files
    if os.path.isdir(file_dir):
        print('\n处理路径：\n%s\n' % file_dir)
        for root, dirs, files in os.walk(file_dir):
            file_info = os.stat(root)
            # https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
            rows = [root, '',
                    datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto'),
                    datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto'), 16]
            yield rows
            for _filename in files:
                if _filename.startswith('.'):
                    continue
                _file = os.path.join(root, _filename)
                file_info = os.stat(_file)
                # print('st_mtime', file_info.st_mtime, os.path.getatime(_file),
                #       datetime.datetime.fromtimestamp(file_info.st_mtime).strftime(str_time),
                #       datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto'))
                # print('st_ctime', file_info.st_ctime, os.path.getctime(_file),
                #       datetime.datetime.fromtimestamp(file_info.st_ctime).strftime(str_time),
                #       datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto'))
                rows = [_file, file_info.st_size,
                        datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto'),
                        datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto'), 0]
                yield rows


def create_efu(file_dir, efu_file=None, encoding='utf-8'):
    if efu_file is None:
        efu_file = '{os.path.basename(file_dir)}.efu'
    writer_efu(efu_file, get_efu_data(file_dir), encoding=encoding)


if __name__ == "__main__":
    from .time import Timer

    t1 = Timer()

    # print(reader_efu(r"file.efu", encoding='utf-8'))
    # create_efu(r'file_dir', efu_file=None, encoding='utf-8')

    t1.running_time()

# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：mycsv.py
#   版本：0.1
#   作者：lds
#   日期：2019-10-11
#   语言：Python 3.X
#   说明：处理 csv 的函数集合
# ---------------------------------------

import os
import csv

import xlwt
import xlsxwriter

from ilds.file import get_encoding


def csv_to_xls(csv_file, delimiter=None):
    """
    cvs 转换为 xls 文件
    """

    # 获取需要导出的文件名
    file_path, file_name = os.path.split(csv_file)
    file_name = os.path.splitext(file_name)[0] + '.xls'
    file_path = os.path.join(file_path, 'xls')
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    xls_file = os.path.join(file_path, file_name)

    print(csv_file, 'to', xls_file)

    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('csv to xls', cell_overwrite_ok=True)

    # with open(csvfile, newline='') as f: # ,encoding='utf-8'
    # print(get_encoding(csvfile))
    encoding = get_encoding(csv_file)
    if encoding.lower() == 'gb2312':
        encoding = 'gbk'
    f = open(csv_file, newline='', encoding=encoding)
    if delimiter is None:
        reader = csv.reader(f)
    else:
        reader = csv.reader(f, delimiter=delimiter)
    xls_sheet = 1
    line = 0
    xls_tite = None
    for row in reader:
        if line == 0:
            if xls_tite is None:
                xls_tite = row
                # print(xls_tite)
        elif line >= 65535:
            line = 0
            xls_sheet += 1
            sheet = workbook.add_sheet('cvs to xls ' + str(xls_sheet), cell_overwrite_ok=True)
            for c, col in enumerate(xls_tite):
                sheet.write(line, c, col.strip())
            line += 1
        for c, col in enumerate(row):
            sheet.write(line, c, col.strip())
        line += 1

    # 关闭文件
    workbook.save(xls_file)
    f.close()

    return xls_file


def csv_to_xlsx(csv_file, delimiter=None):
    """
    cvs 转换为 xlsx 文件
    """

    # 获取需要导出的文件名
    file_path, file_name = os.path.split(csv_file)
    file_name = os.path.splitext(file_name)[0] + '.xlsx'
    file_path = os.path.join(file_path, 'xlsx')
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    xlsx_file = os.path.join(file_path, file_name)

    print(csv_file, 'to', xlsx_file)

    workbook = xlsxwriter.Workbook(xlsx_file)
    worksheet = workbook.add_worksheet()
    worksheet.name = 'cvs to xlsx'

    # with open(csvfile, newline='') as f: # ,encoding='utf-8'
    encoding = get_encoding(csv_file)
    if encoding.lower() == 'gb2312':
        encoding = 'gbk'
    f = open(csv_file, newline='', encoding=encoding)
    if delimiter is None:
        reader = csv.reader(f)
    else:
        reader = csv.reader(f, delimiter=delimiter)

    line = 0
    for row in reader:
        # print(row, len(row))
        for i, cell in enumerate(row):
            # print(cell)
            cell = cell.strip()
            # print(cell)
            worksheet.write(line, i, cell)
        line += 1
    workbook.close()
    f.close()

    return xlsx_file


if __name__ == '__main__':
    from ilds.time import Timer

    with Timer() as timer:
        ...
        csv_to_xls(r"D:\2019-10-11 16-34-44.csv", delimiter=None)
        csv_to_xlsx(r"D:\2019-10-11 16-34-44.csv", delimiter=None)

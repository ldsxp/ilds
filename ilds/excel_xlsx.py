﻿# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：excel_xlsx.py
#   版本：0.1
#   作者：lds
#   日期：2018-7-31
#   语言：Python 3.X
#   说明：读取excel文件内容
# ---------------------------------------

from time import time
from warnings import warn

# ReadExcel
from openpyxl import load_workbook
from openpyxl.styles import numbers, is_date_format

(
    XL_CELL_EMPTY,
    XL_CELL_TEXT,
    XL_CELL_NUMBER,
    XL_CELL_DATE,
    XL_CELL_BOOLEAN,
    XL_CELL_ERROR,
    XL_CELL_BLANK,
) = range(7)


class ReadXlsx(object):

    def __init__(self, *args, **kwargs):
        """
        读取 Excel 文件的类 用 openpyxl 重写

        # 例子
        xlsx_file = r"E:\my - 数据\其他\20180731 阿玲 参考\申请单G1.5(1)(1).xlsx"
        # xlsx = ReadExcel(xlsx_file, data_only=True) # data_only=True 的时候不读取公式 , index=10

        xlsx = ReadXlsx(xlsx_file)
        # time_fmt = "%Y-%m"
        xlsx.debug = True
        # print(xlsx.sheet_names)

        for i in range(len(xlsx.sheet_names)):
            xlsx.max_row
            xlsx.max_column
            print('next_sheet ---------------------------------')
            xlsx.next_sheet()

        # print(xlsx.datasets())
        # for i in xlsx.datasets():
        #     print(i)

        # for i in xlsx.values():
        #     print(i)

        print(xlsx.set_sheet(10)) # 这个要判断下是否成功
        print(xlsx.next_sheet(), xlsx.index)

        print(xlsx.title)

        """
        # print('args', args,'kwargs',kwargs)

        # 打开的表索引
        try:
            self.index = kwargs.pop('index')
        except:
            self.index = 0

        # 数字转字符串

        # 日期格式
        self.time_fmt = "%Y-%m-%d"
            # self.time_fmt = "%Y-%m"

        # self.excel = 'xlsx'
        self.wb = load_workbook(*args,**kwargs)
        self.sheet_names = self.wb.sheetnames
        self.set_sheet(self.index)
        # print(self.excel)

        self.debug = False

    @property
    def title(self):
        """  标题 """
        return self.sheet_names[self.index]

    @property
    def max_row(self):
        """  行 """
        if self.debug: print(f"title {self.title} index {self.index} 行 {self.sheet.max_row}")
        return self.sheet.max_row

    @property
    def max_column(self):
        """  列 """
        if self.debug:print(f"title {self.title} index {self.index} 列 {self.sheet.max_column}")
        return self.sheet.max_column

    # @property
    def datasets(self):
        """
        sheet 的数据集（列表）
        xls 的表达式不能显示
        """
        return list(self.values())

    def values(self):
        """
        sheet 的数据集（列表）
        xlsx 空表格是 None
        xls  空表格是 ''
        xlsx 0 是 0
        xls  0 是 0.0
        xls 的表达式不能显示
        # 返回可迭代结果
        """
        # rows 是可迭代的生成器
        for row in self.sheet.rows:
            row_vals = []
            # row_vals = [c.value for c in row]
            # print(row)
            for c in row:
                if c.data_type == "n" :
                    if c.number_format != "General" and is_date_format(c.number_format):
                        # print('number_format 日期',c.number_format,c.value)
                        if c.value is not None:
                            cell_value = c.value.strftime(self.time_fmt)
                        else:
                            cell_value = ''
                    else:
                        if c.value is not None:
                            cell_value = str(c.value)  # 数字转换为字符串
                        else:
                            cell_value = 0
                else:
                    cell_value = c.value
                row_vals.append(cell_value)
            # print(row_vals)
            yield row_vals

    def next_sheet(self):
        """ 下一个表 """
        return self.set_sheet(self.index + 1)

    def set_sheet(self, index=None):
        """ 设置表 """

        if index is not None:
            # 这里判断是否超过范围 调试了很久 ， 因为索引是从0开始的 啊 啊 啊 啊 啊
            if len(self.sheet_names) >= index + 1:
                self.index = index
            else:
                # WarningInfo = "访问的表 %s 不存在" % index
                # warn(WarningInfo)
                # if self.index == index: # 初始化设置的不存在的表
                #     self.index = 0
                return None

        self.sheet = self.wb[self.sheet_names[self.index]]

        return self.index


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=ReadXlsx)

    print(doc_text)

if __name__ == "__main__":
    t1 = time()

    # 例子
    xlsx_file = r"E:\my - 数据\其他\20180731 阿玲 参考\申请单G1.5(1)(1).xlsx"
    # xlsx = ReadExcel(xlsx_file, data_only=True) # data_only=True 的时候不读取公式 , index=10

    xlsx = ReadXlsx(xlsx_file)
    # time_fmt = "%Y-%m"
    xlsx.debug = True
    # print(xlsx.sheet_names)

    for i in range(len(xlsx.sheet_names)):
        xlsx.max_row
        xlsx.max_column
        print('next_sheet ---------------------------------')
        xlsx.next_sheet()

    # print(xlsx.datasets())
    # for i in xlsx.datasets():
    #     print(i)

    # for i in xlsx.values():
    #     print(i)

    print(xlsx.set_sheet(10)) # 这个要判断下是否成功
    print(xlsx.next_sheet(), xlsx.index)

    print(xlsx.title)

    print('用时 %.2f 秒' % (time() - t1))



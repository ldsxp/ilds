# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：excel_xlrd.py
#   版本：0.1
#   作者：lds
#   日期：2018-7-24
#   语言：Python 3.X
#   说明：读取excel文件内容
# ---------------------------------------

from time import time
from warnings import warn

# ReadExcel
import xlrd

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
        读取 Excel 文件的类

        xls_file = r"(数据库标准格式20180424）2.xlsx"

        xls = ReadXlsx(xls_file)
        # time_fmt = "%Y-%m"
        print(xls.sheet_names)
        print(xls.title)
        print(xls.max_row)
        print(xls.max_column)

        # print(xls.datasets)
        # for i in xls.datasets:
        #     print(i)

        for i in xls.values():
            print(i)

        # print(xls.set_sheet(10)) # 这个要判断下是否成功
        print('next_sheet ---------------------------------')
        print(xls.next_sheet(),xls.index)
        print(xls.title)


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

        self.excel = 'xls'
        self.wb = xlrd.open_workbook(*args,**kwargs)
        self.sheet_names = self.wb.sheet_names()
        self.set_sheet(self.index)
        # print(self.excel)

    @property
    def title(self):
        """  标题 """
        return self.sheet_names#[self.index]

    @property
    def max_row(self):
        """  行 """
        return self.sheet.nrows

    @property
    def max_column(self):
        """  列 """
        return self.sheet.ncols

    @property
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

        """
        # 遍历 sheet 中所有行row
        for row_index in range(self.sheet.nrows):
            # row_vals = self.sheet.row_values(row_index)
            # print('row %s is %s' % (curr_row, row_vals))
            row_vals = []
            for col_index in range(self.sheet.ncols):
                cell = self.sheet.cell(row_index, col_index)
                # print(xlrd.cellname(row_index, col_index), '-', end=' ')
                # print(cell.value, '-', end=' ')
                # print(cell.ctype)
                if XL_CELL_DATE == cell.ctype:
                    # 把 excel 时间格式转化为 字符串
                    cell_value =  xlrd.xldate.xldate_as_datetime(cell.value, 0).strftime(self.time_fmt)
                    # print('XL_CELL_DATE',cell_value)
                elif XL_CELL_NUMBER == cell.ctype:
                    # 把 excel 数字转换为 字符串
                    if cell.value == int(cell.value):  # 检查是不是整数:
                        cell_value = str(int(cell.value))
                    else:
                        cell_value = str(cell.value)
                    # print('XL_CELL_NUMBER', cell.value,cell_value)
                elif XL_CELL_EMPTY == cell.ctype:
                    # 把 excel 空字符转换为 字符串 None
                    cell_value = ''
                    # print('XL_CELL_EMPTY', cell.value)
                else:
                    cell_value = cell.value
                row_vals.append(cell_value)
            yield row_vals

    def next_sheet(self):
        """ 下一个表 """
        return self.set_sheet(self.index + 1)

    def set_sheet(self,index=None):
        """ 设置表 """

        if index is not None:
            # 这里判断是否超过范围 调试了很久 ， 因为索引是从0开始的 啊 啊 啊 啊 啊
            if len(self.sheet_names) >= index + 1:
                self.index = index
            else:
                WarningInfo = "访问的表 %s 不存在" % index
                warn(WarningInfo)
                # if self.index == index: # 初始化设置的不存在的表
                #     self.index = 0
                return None

        self.sheet = self.wb.sheets()[self.index]

        return self.index


def xlrd_string(xlrdfloat):
    """转换 excel 的浮点数到字符串"""
    if xlrdfloat == int(xlrdfloat):  # 检查是不是整数:
        s = str(int(xlrdfloat))
    else:
        s = str(xlrdfloat)
    # s = str(cell.value)
    # s = float(cell.value)
    return s


def gequ_re(gequ):
    """处理歌曲名称
    最后修改时间：20181015
    """
    try:
        gequ = gequ.replace('	', ' ').replace('(', '（').replace(')', '）').replace('\n', '')\
            .replace('|', '/').replace(' ', ' ').replace(' （', '（')\
            .replace('  ', ' ').replace('  ', ' ').strip()
        # .replace('/', ' ').replace('+', ' ')
    except Exception as e:
        if isinstance(gequ, float):
            gequ = xlrd_string(gequ)
        else:
            print('问题：------------------- 歌名：%s -------------------' % (gequ))
    return gequ


def geshou_re(geshou):
    """处理表演者
    最后修改时间：20181015
    """
    geshou = geshou.replace('+', ' ').replace('/', ' ').replace('	', ' ').replace('(', '（').replace(
        ')', '）').replace('&', ' ').replace('|', ' ').replace('•', '·') \
        .replace('；', ' ').replace('\n', '').replace(',', ' ').replace(' ', ' ').replace(' （', '（')\
        .replace('  ', ' ').replace('  ', ' ').strip()
    if "（" in geshou:
        return geshou
    else:
        return geshou.replace('、', ' ').replace('  ', ' ')


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=ReadXlsx)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=xlrd_string)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=gequ_re)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=geshou_re)

    print(doc_text)

if __name__ == "__main__":
    t1 = time()
    xls_file = r"(数据库标准格式20180424）2.xlsx"

    xls = ReadXlsx(xls_file)
    # time_fmt = "%Y-%m"
    print(xls.sheet_names)
    print(xls.title)
    print(xls.max_row)
    print(xls.max_column)

    # print(xls.datasets)
    # for i in xls.datasets:
    #     print(i)

    for i in xls.values():
        print(i)

    # print(xls.set_sheet(10)) # 这个要判断下是否成功
    print('next_sheet ---------------------------------')
    print(xls.next_sheet(),xls.index)
    print(xls.title)

    print('用时 %.2f 秒' % (time() - t1))



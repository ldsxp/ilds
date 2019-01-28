# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：pd.py
#   版本：0.1
#   作者：lds
#   日期：2019-01-28
#   语言：Python 3.X
#   说明：pandas 常用的函数集合，TODO 添加一些小抄在这里！
# ---------------------------------------


def get_columns_index(df, columns):
    """获取列名称在 DataFrame 中的索引"""
    if isinstance(columns, str):
        columns = [columns]
    columns_index = []
    for col in columns:
        columns_index.append(df.columns.get_loc(col))
    # print('columns_index', columns_index)
    return columns_index


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

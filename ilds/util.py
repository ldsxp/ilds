# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：util.py
#   版本：0.5
#   作者：lds
#   日期：2022-01-16
#   语言：Python 3.X
#   说明：常用的函数集合
# ---------------------------------------
import os.path

from ilds.lib.configobj import ConfigObj

# 最后修改时间：20190929
CLEAN_STR = "	", " ", "(", ")", "（", "）", " ", "|", "/", "+", "&", "•", "；", " ", "＆", "　", "<", ">" \
    , "、", "\n", "\"", "?", "？", "*", ",", "《", "》", "-", "×", "."

# 替换的字符串
REPLACE_LIST = [("remix", "dj"), ("dj版", "dj")]


def print_doc(fun, is_all=True):
    """
    打印函数的文档信息
    """
    siyou = []
    siyou2 = []
    doc = []
    for name in dir(fun):
        if name.startswith('__'):
            if len(siyou) % 6 == 0:
                siyou.append('\n')
            siyou.append(name)

        elif name.startswith('_'):
            if len(siyou2) % 6 == 0:
                siyou2.append('\n')
            siyou2.append(name)
        else:
            if is_all:
                doc.append("%s " % name + "-" * 78)
                doc.append(str(eval("fun.%s.__doc__" % name)))
                doc.append("=" * 78 + " %s\n" % name)
            else:
                doc.append(name)

    print(' '.join(siyou))
    print(' '.join(siyou2))
    print('\n'.join(doc))


def prints(frame, *args):
    """
    打印的时候，包括当前行信息，方便 pycharm 直接跳转到当前位置
    例子：
    prints(sys._getframe(), 1, dict)
    """
    print(f'File "{frame.f_code.co_filename}", line {frame.f_lineno}, {frame.f_code.co_name}\n   ', *args)


def dict_val_to_key(mydict):
    """
    字典键值互换
    """
    return dict([val, key] for key, val in mydict.items())


def list_to_dict(list1, list2):
    """
    把两个列表转换成相对应的字典
    """
    ku_field_row_dict = {}
    for i in range(len(list1)):
        # print(list1[i], list2[i])
        ku_field_row_dict[list1[i]] = list2[i]
    return ku_field_row_dict


def sort_dict(dict_, reverse=False):
    """
    按字典（键）重新排序
    :param dict_: 字典
    :param reverse: 排序方式 True False
    :return: 排序好的字典
    """
    dict_sort = {}

    for k in sorted(dict_.keys(), reverse=reverse):
        dict_sort[k] = dict_[k]

    return dict_sort


def get_kuohao_feijie(value):
    """
    输入带括号内容的内容 返回内容 和 括号内内容
    """
    str_kuohao = value.strip()
    if ("（") in str_kuohao:
        if "）" in str_kuohao:
            pos1 = str_kuohao.index("（")
            pos2 = str_kuohao.index("）")
            # print(pos1)
            # print(pos2)
            # print(len(str_kuohao))
            if (pos2 + 1) == len(str_kuohao):
                kuohao1 = str_kuohao[: pos1].strip()
                kuohao2 = str_kuohao[pos1 + 1: pos2].strip()
                return kuohao1, kuohao2
            else:
                print("歌曲括号后面有内容", value)
                return value
                #
        else:
            print("歌曲括号不匹配", value)
            return value


def xl_col_to_name(col_num, col_abs=False):
    """
    将零索引列单元格引用转换为字符串。

    来自 ： xlsxwriter 中的 utility.py

    Args:
       col:     列 数字
       col_abs: 用于使列绝对的可选标志。布尔。

    Returns:
        列样式字符串。

    """
    col_num += 1  # 改为 1-index.
    col_str = ''
    col_abs = '$' if col_abs else ''

    while col_num:
        # 提醒从 1 .. 26 设置序号
        remainder = col_num % 26

        if remainder == 0:
            remainder = 26

        # 将余数转换为字符。
        col_letter = chr(ord('A') + remainder - 1)

        # 从右到左累积列字母。
        col_str = col_letter + col_str

        # 获得下一个数量级
        col_num = int((col_num - 1) / 26)

    return col_abs + col_str


def get_config(file="./config.ini", key='file', ret_obj=False, default=''):
    """
    获取ini中的内容
    :param file: ini 文件
    :param key: 要读取的键
    :param ret_obj: 如果为真，返回元组（config 对象，值）
    :return: 根据 ret_obj 参数返回值或（config 对象，值）

    例子：
    config, value = get_config(file="./config.ini", key='file', ret_obj=True)
    print(config, value)

    # 添加新项
    config['files'] = []
    config['files'].append("我们是中文的")

    # 读配置文件
    print(config['files'])

    # 保存配置文件
    config.write()

    # 删除项
    # del config['files']

    # 将配置写入到不同的文件
    # config.filename = "./test1.ini"
    # config.write()
    """

    config = ConfigObj(file, encoding='utf-8')

    _value = config.get(key, ConfigObj)

    # 如果没有找到内容我们设置一个默认值
    if _value == ConfigObj:
        _value = config[key] = default
        config.write()

    if ret_obj:
        return config, _value
    else:
        return _value


def cleaning_str(text, replace_list=None, reorder_string=False):
    """
    清理字符中的多余符号

    :param text: 要处理的文本
    :param replace_list: 替换指定的字符
    :param reorder_string:重新排序字符串
    :return:
    """

    temp = text.strip().lower()

    # 替换内容
    if replace_list is None:
        replace_list = REPLACE_LIST
    # print('替换内容', replace_list)
    for ch in replace_list:
        temp = temp.replace(*ch)

    # 重新排序
    if reorder_string:
        temp = ''.join(sorted(temp))

    # 清除符号
    for ch in CLEAN_STR:
        temp = temp.replace(ch, '')

    return temp


def cleaning_digital(_str):
    """
    清理数字中的标点符号后面的数字
    """
    return str(int(str(_str).split('.')[0])).strip()


class attrdict(dict):
    """
    可以用属性访问的字典
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


def check_out(exit_file='lds.exit'):
    """
    检查标记退出的文件是否存在，存在的时候删除文件，并返回 True
    :param exit_file:
    :return:
    """
    if os.path.exists(exit_file):
        os.remove(exit_file)
        return True


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=print_doc)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=prints)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=dict_val_to_key)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=list_to_dict)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=sort_dict)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_kuohao_feijie)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=xl_col_to_name)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_config)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

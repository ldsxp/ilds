# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：myjson.py
#   版本：0.1
#   作者：lds
#   日期：2018-7-4
#   语言：Python 3.X
#   说明：处理 json 的函数集合
# ---------------------------------------

import os
import json


def json_read(path):
    """
    读取 json 文件
    """
    try:
        if not os.path.exists(path):
            return False
        with open(path, 'r', encoding='utf-8') as f:
            obj = json.load(f)
        return obj
    except Exception as e:
        print('json_read',e)
        return False


def json_save(obj, path):
    """
    保存 json 文件
    """

    if obj is None:
        return False
    else:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print('json_save', e)
            return False


def doc():
    """
    打印模块说明文档
    """
    doc_text = """
    """
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=json_read)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=json_save)

    print(doc_text)


if __name__ == '__main__':

    # 记录运行时间 --------------------------------------------------
    from time import time, sleep
    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

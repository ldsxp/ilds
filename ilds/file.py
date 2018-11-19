# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：file.py
#   版本：0.3
#   作者：lds
#   日期：2018-10-23
#   语言：Python 3.X
#   说明：常用的文件操作函数集合
# ---------------------------------------


import os
import sys
import random
import shutil
# get_file_md5
import hashlib
# get_encoding
import chardet
# validateTitle
import re
from datetime import datetime


def is_file(filename):
    """
    判断是否为文件
    :param filename:文件
    :return:文件不存在，不是文件，大小为0，返回 None
    """
    if not os.path.exists(filename):
        print(filename, ' 没有找到')
        return None
    if not os.path.isfile(filename):
        print(filename, ' 不是文件')
        return None
    if os.path.getsize(filename) == 0:
        print(filename, ' 大小为 0')
        return None

    return filename


def make_dir(_path):
    """
    检查文件目录是否存在，如果不存在则创建。
    """
    if not os.path.exists(_path):
        os.makedirs(_path)


def exist_or_makedir(in_dir):
    """
    检查文件所在的父级文件夹是否存在，如果不存在，就创建父级文件夹
    :param in_dir:
    :return: None
    """
    output_dir = os.path.dirname(in_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        return output_dir


def get_encoding(fromfile):
    """
    文件编码判断
    :param fromfile: 
    :return: 编码格式
    """
    with open(fromfile, 'rb') as tt:
        ff = tt.readline()
        # 这里试着换成read(5)也可以，但是换成readlines()后报错
        enc = chardet.detect(ff)
        # print(enc['encoding'])
        return (enc['encoding'])


def validate_title(title):
    """
    去除文件名中的非法字符 (Windows)
    :param title:
    :return:
    """
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    # 替换为空格，也可以替换为“_”
    new_title = re.sub(rstr, " ", title)
    return new_title


def replace_invalid_filename_char(filename, replaced_char='_'):
    """
    替换文件名中无效的字符。 默认用'_'替换。

    :param filename:  要替换的文件名
    :param replaced_char:  替换的字符
    :return:
    """
    invalid_characaters = '\\/:*?"<>|'
    for c in invalid_characaters:
        filename = filename.replace(c, replaced_char)

    return filename


def get_file_md5(filename):
    """
    计算文件的 MD5
    :param filename:
    :return:
    """

    if not is_file(filename):
        return None

    md5_ = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_.update(data)
    return md5_.hexdigest()


def get_text_md5(text):
    """
    计算文件的 MD5
    :param filename:
    :return:
    """
    return hashlib.md5(text. encode('utf-8')).hexdigest()


def from_this_dir(filename):
    """
    获取运行模块所在路径的全路径
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)


def from_this_dir_2(filename):
    """
    获取本模块所在路径的全路径
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def get_file_line_info():
    """ 获取当前时间，文件路径，所在行数"""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    # print(dir(f))
    return '%s, File "%s", line %s ' % (
        str(datetime.now()), f.f_code.co_filename, str(f.f_lineno)
    )
    # , f.f_code.co_name(<module>)


def file_string_replace(file, old, new, count=None):
    """
    按行替换文件内容
    """

    counts = 0
    with open(file, "r", encoding="utf-8") as f:
        # readlines以列表的形式将文件读出
        lines = f.readlines()
    with open(file, "w", encoding="utf-8") as f_w:
        # 定义一个数字，用来记录在读取文件时在列表中的位置
        n = 0
        # 默认选项，只替换第一次匹配到的行中的字符串
        for line in lines:
            if old in line:
                counts += 1
                line = line.replace(old, new)
            f_w.write(line)

    if counts:
        print("在 %s 中替换了 %s 为 %s，总共 %s个" % (file, old, new,counts))
    else:
        print("没有内容替换")


def exists_file(_file):
    """
    判断文件是否存在，如果存在就返回重命名的文件，不存在就直接返回
    :param _file:
    :return:
    """
    if os.path.exists(_file):
        while True:
            f_name, f_ext = os.path.splitext(_file)
            _file2 = f_name + '-' + str(random.randint(0, 10000000)) + f_ext
            if _file != _file2:
                break
        return _file2
    else:
        return _file


def exists_file_to_bak(_file):
    """
    如果文件已经存在，拷贝到 bak 文件夹
    """
    if os.path.exists(_file):
        while True:
            file_path, file_name = os.path.split(_file)
            f_name, f_ext = os.path.splitext(file_name)
            _file2 = os.path.join(file_path, 'bak',f_name + '-' + datetime.now().strftime('%Y%m%d%H%M%S') + f_ext)
            if _file != _file2:
                break
        make_dir(os.path.dirname(_file2))
        shutil.move(_file, _file2)
        # print(shutil.move(_file, _file2))
        # print((_file, _file2))


def get_name(path):
    """
    获取路径中最后的文件名 不包括后缀名
    """
    # 分离路径的目录名和文件名(dirname(), basename()) 元组，后一部分总是最后级别的目录或文件名
    _, name = os.path.split(path)
    # 分离文件名和扩展名， 返回(filename,extension)元组，没有扩展名，扩展名返回空
    ret_name, _ = os.path.splitext(name)
    return ret_name


def from_dir_func(dir_path, func, endswith='', *args, **kwargs):
    """
    处理目录中的所有文件，跳过前缀是.的文件名

    # 扩展阅读
    from functools import partial
    基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。
    使用这个函数可以把接受一个或多个参数的函数改编成需要回调的 API，这样参数更少。
    new_func = partial(test, 22222)
    """

    fileok = 0
    fileno = 0
    if os.path.isdir(dir_path):
        print('\n处理路径：\n%s\n' % (dir_path))
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for _filename in filenames:
                if _filename.startswith('.'):
                    continue

                _file = os.path.join(dirpath, _filename)
                if endswith:
                    if _file.endswith(endswith):
                        fileok += 1
                        # print(_file)
                        func(_file, *args, **kwargs)
                    else:
                        fileno += 1
                        # print('忽略 --------------------', _file)
                else:
                    fileok += 1
                    func(_file)

        print(' ----------- 处理 %s 个文件（处理条件：%s） ----------- 忽略 %s 个文件 ----------- ' % (fileok, endswith, fileno))
    else:
        print('请输入文件路径！')


def get_walk_files(dir_path, endswith=''):
    """
    获取文件夹包括子文件夹里面的文件列表（生成器）
    """
    if os.path.isdir(dir_path):
        print('\n处理路径：\n%s\n' % (dir_path))
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for _filename in filenames:
                if _filename.startswith('.'):
                    continue

                _file = os.path.join(dirpath, _filename)
                if endswith:
                    if _file.endswith(endswith):
                        yield _file
                else:
                    yield _file
    else:
        return None


def get_dir_files(path, ext=''):
    """
    获取文件夹里面，指定后缀名的文件列表（生成器）
    例子：
    get_dir_files(r".",'py')
    """
    # files = []
    for _file in os.listdir(path):
        if _file.endswith(ext):
            file_path = os.path.join(path, _file)
            if os.path.isfile(file_path):
                # files.append(file_path)
                yield file_path
                # print(_file)
    # return files


def doc():
    """
    打印模块说明文档
    """
    doc_text = """
    # 默认字典的例子
    from collections import defaultdict
    def get_counts2(sequence):
        counts = defaultdict(int) # 所有的值均会被初始化为0
        for x in sequence:
            counts[x] += 1
        return counts
    
    """
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=is_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=make_dir)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=exist_or_makedir)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_encoding)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=validate_title)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=replace_invalid_filename_char)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_md5)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_text_md5)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_this_dir)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_this_dir_2)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_line_info)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=file_string_replace)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=exists_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=exists_file_to_bak)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_name)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_dir_func)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    # 性能测试
    # from timeit import timeit
    # print(timeit('validate_title("\\fasdf/f:*?dasfdddddddddddddddddddddda<fasf>|")', 'from file import validate_title', number=1000000))
    # replace_invalid_filename_char 稍微快一点
    # print(timeit('replace_invalid_filename_char("\\fasdf/f:*?dasfdddddddddddddddddddddda<fasf>|")', 'from file import replace_invalid_filename_char', number=1000000))

    print('运行时间 %.2f 秒' % (time() - start_time))

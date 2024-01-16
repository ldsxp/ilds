# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：file.py
#   版本：0.9
#   作者：lds
#   日期：2020-12-05
#   语言：Python 3.X
#   说明：常用的文件操作函数集合
# ---------------------------------------


import os
import sys
import json
import random
import shutil
# get_file_md5
import hashlib
# get_encoding
import chardet
from chardet.universaldetector import UniversalDetector
# validateTitle
import re
from datetime import datetime
from zlib import crc32
import difflib
import warnings

from colorama import Fore, Back, Style

AFILES = []  # EE
BFILES = []  # SVN
COMMON = []  # EE & SVN


# import _winapi #  可以创建文件夹的软链接
# _winapi.CreateJunction(r"源文件", r"链接文件")

def is_file(file):
    """
    判断是否为文件
    :param file:文件
    :return:文件不存在，不是文件，大小为0，返回 None
    """
    if not os.path.exists(file):
        print(file, ' 没有找到')
        return None
    if not os.path.isfile(file):
        print(file, ' 不是文件')
        return None
    if os.path.getsize(file) == 0:
        print(file, ' 大小为 0')
        return None

    return file


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
    warnings.warn('exist_or_makedir 已经弃用，建议用 os.makedirs(name, exist_ok=True) 替代',
                  DeprecationWarning)
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
    with open(fromfile, 'rb') as f:
        detector = UniversalDetector()
        for line in f:
            detector.feed(line)
            if detector.done: break
        detector.close()
        return detector.result['encoding']


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


def replace_invalid_filename_char(filename, replaced_char='_', max=100):
    """
    替换文件名中无效的字符。 默认用'_'替换。

    :param filename:  要替换的文件名
    :param replaced_char:  替换的字符
    :return:
    """
    invalid_characaters = '\\/:*?"<>|\r\n\t'
    for c in invalid_characaters:
        filename = filename.replace(c, replaced_char)

    # 清理空白符号
    filename = filename.strip()

    # 截断超过最大长度的字符
    if len(filename) > max:
        filename = f'{filename[:max - 3]}……'

    return filename


def get_file_crc32(file):
    """
    计算文件的 CRC32
    :param file:
    :return:
    """
    with open(file, 'rb') as f:
        return crc32(f.read())


def get_file_md5(file, block_size=65536):
    """
    计算文件的 MD5
    :param file: 文件路径
    :param block_size: 读取缓存大小
    :return:
    """

    if not is_file(file):
        return None

    md5_ = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            md5_.update(buf)
    return md5_.hexdigest()


def get_hash_sums(file, names=None, block_size=65536):
    """
    获取文件的哈希信息

    :param file: 文件路径
    :param names: 要获取的哈希名字列表
    :param block_size: 读取缓存大小
    :return:
    """
    _hash_sums = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha224': hashlib.sha224(),
        'sha256': hashlib.sha256(),
        'sha384': hashlib.sha384(),
        'sha512': hashlib.sha512()
    }
    if names is None:
        hash_sums = _hash_sums
    else:
        hash_sums = {k: v for k, v in _hash_sums.items() if k in names}
        if not hash_sums:
            return

    with open(file, 'rb') as fd:
        data_chunk = fd.read(block_size)
        while data_chunk:
            for hash_sum in hash_sums.keys():
                hash_sums[hash_sum].update(data_chunk)
            data_chunk = fd.read(block_size)

    results = {}
    for key, value in hash_sums.items():
        results[key] = value.hexdigest()
    return results


def get_file_hash(file, block_size=65536, hash_calc=None):
    """
    计算文件的哈希

    :param file: 文件路径
    :param block_size: 读取缓存大小
    :param hash_calc: 哈希算法（md5、sha1、sha224、sha256、sha384、sha512等）
    :return: 文件哈希

    """

    if not is_file(file):
        return None

    if hash_calc is None:
        hash_calc = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            hash_calc.update(buf)
    return hash_calc.hexdigest()


def get_hash(file_path, block_size=65536):
    """
    获取文件哈希信息

    :param file_path: 文件路径
    :param block_size: 读取缓存大小
    :return: {'md5', '', 'sha1', '', 'hash', '', }
    """

    calc_md5 = hashlib.md5()
    calc_sha1 = hashlib.sha1()
    calc_hash = hashlib.sha256()

    with open(file_path, 'rb') as fd:
        data_chunk = fd.read(block_size)
        while data_chunk:
            calc_md5.update(data_chunk)
            calc_sha1.update(data_chunk)
            calc_hash.update(data_chunk)
            data_chunk = fd.read(block_size)

    results = {
        'md5': calc_md5.hexdigest(),
        'sha1': calc_sha1.hexdigest(),
        'hash': f'sha256:{calc_hash.hexdigest()}',  # sha256[哈希算法名字，统一用小写]:[分隔符]128[哈希]，最多字符数 136
    }

    return results


def get_text_md5(text):
    """
    计算文件的 MD5
    :param filename:
    :return:
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def human_size(sz):
    """
    以人类可读的格式返回大小
    """
    if not sz:
        return False
    units = ('bytes', 'Kb', 'Mb', 'Gb')
    s, i = float(sz), 0
    while s >= 1024 and i < len(units) - 1:
        s /= 1024
        i += 1
    return "%0.2f %s" % (s, units[i])


def from_this_dir(file):
    """
    获取运行模块所在路径的全路径
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), file)


def from_this_dir_2(file):
    """
    获取本模块所在路径的全路径
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)


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
        print("在 %s 中替换了 %s 为 %s，总共 %s个" % (file, old, new, counts))
    else:
        print("没有内容替换")


def exists_file(_file):
    """
    判断文件是否存在，如果存在就返回重命名的文件，不存在就直接返回
    :param _file:
    :return:
    """

    warnings.warn(
        'exists_file 已经弃用，因为它对人类不友好，也没有检查新名字是否已经存在\n建议用 check_filename_available 替代',
        DeprecationWarning)

    if os.path.exists(_file):
        while True:
            f_name, f_ext = os.path.splitext(_file)
            _file2 = f_name + '-' + str(random.randint(0, 10000000)) + f_ext
            if _file != _file2:
                break
        return _file2
    else:
        return _file


def check_filename_available(file, make_dirs=False, dirs_name='重复'):
    """
    检查文件是否存在，如果已经存在，添加编号重命名或者创建重复内容的文件夹
    例如: 文件.txt > 文件 (1).txt
          文件.txt > 重复(1)/文件.txt

    :param file: 要检查的文件
    :param make_dirs: 是否创建文件夹
    :param dirs_name: 文件夹的名字
    :return: 不重复的文件路径
    """
    import os
    if not os.path.exists(file):
        return file

    num = 1
    if make_dirs:
        f_path, f_file = os.path.split(file)
    else:
        f_name, f_ext = os.path.splitext(file)
    while True:
        if make_dirs:
            new_file_name = os.path.join(f_path, f"{dirs_name}({num})", f_file)
        else:
            new_file_name = f"{f_name} ({num}){f_ext}"
        if not os.path.exists(new_file_name):
            return new_file_name
        num += 1


def exists_file_to_bak(file):
    """
    如果文件已经存在，拷贝到 bak 文件夹
    """
    if os.path.exists(file):
        while True:
            file_path, file_name = os.path.split(file)
            f_name, f_ext = os.path.splitext(file_name)
            _file2 = os.path.join(file_path, 'bak', f_name + '-' + datetime.now().strftime('%Y%m%d%H%M%S') + f_ext)
            if file != _file2:
                break
        make_dir(os.path.dirname(_file2))
        shutil.move(file, _file2)
        # print(shutil.move(_file, _file2))
        # print((_file, _file2))


def get_name(file):
    """
    获取路径中最后的文件名 不包括后缀名
    """
    # os.path.split 分离路径的目录名和文件名(dirname(), basename()) 元组，后一部分总是最后级别的目录或文件名
    _, name = os.path.basename(file)
    # 分离文件名和扩展名， 返回(filename,extension)元组，没有扩展名，扩展名返回空
    ret_name, _ = os.path.splitext(name)
    return ret_name


def list_dir(file_dir):
    """
    获取文件夹下的文件列表
    跳过目录、文件名前缀是.的文件

    :param file_dir:
    :return: 返回文件列表的生成器
    """
    if os.path.isdir(file_dir):
        for name in os.listdir(file_dir):
            file = os.path.join(file_dir, name)

            # 跳过目录
            if os.path.isdir(file):
                continue

            # 跳过文件名前缀是.的文件
            if name.startswith('.'):
                continue

            # print(file)
            yield file
    else:
        raise NotADirectoryError(file_dir)


def from_dir_func(dir_path, func, prefix='.', suffix='', *args, **kwargs):
    """

    处理目录中的所有文件，默认跳过前缀是.的文件名，返回函数运行结果

    # 扩展阅读
    from functools import partial
    基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。
    使用这个函数可以把接受一个或多个参数的函数改编成需要回调的 API，这样参数更少。
    new_func = partial(test, 22222)

    :param dir_path:
    :param func:
    :param prefix: 默认跳过前缀是.的文件名
    :param suffix: 只处理后缀匹配的文件
    :param args:
    :param kwargs:
    :return: 返回函数运行结果的信息
    """

    fileok = 0
    fileno = 0
    info = []
    if os.path.isdir(dir_path):
        print('\n处理路径：\n%s\n' % (dir_path))
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for _filename in filenames:
                if prefix and _filename.startswith(prefix):
                    continue

                _file = os.path.join(dirpath, _filename)
                if suffix:
                    if _file.endswith(suffix):
                        fileok += 1
                        # print(_file)
                        info.append(func(_file, *args, **kwargs))
                    else:
                        fileno += 1
                        # print('忽略 --------------------', _file)
                else:
                    fileok += 1
                    info.append(func(_file, *args, **kwargs))

        print(
            ' ----------- 处理 %s 个文件（跳过名称前面是：“%s”，处理后缀：“%s”） ----------- 忽略 %s 个文件 ----------- ' % (
                fileok, prefix, suffix, fileno))
    else:
        raise FileExistsError('请输入文件路径！')
    return info


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


def save_file(s, file, mode='w', encoding='utf-8'):
    """保存字符内容到文件"""
    with open(file, mode, encoding=encoding) as fp:
        fp.write(s)


def dir_compare(apath, bpath, diff_ext=None, out_dir=None):
    """
    比较两个目录的文件差异

    例子：
    diff_ext = ['.md']
    dir_compare(FolderEE, FolderSVN, diff_ext)

    :param apath:
    :param bpath:
    :param diff_ext:
    :return:
    """

    if diff_ext is None:
        diff_ext = []

    if out_dir is None:
        out_dir = os.getcwd()

    afiles = []
    bfiles = []
    for root, dirs, files in os.walk(apath):
        # print(apath, '所有文件数量：', len(files))
        for f in files:
            # 比较文件名不含格式后缀
            # afiles.append(root + f[0:-4])
            # 比较文件名含格式后缀
            afiles.append(os.path.join(root, f))

    for root, dirs, files in os.walk(bpath):
        # print(bpath, '所有文件数量：', len(files))
        for f in files:
            # 比较文件名不含格式后缀
            # bfiles.append(root + f[0:-4])

            # 比较文件名含格式后缀
            bfiles.append(os.path.join(root, f))
            # sizeB = os.path.getsize(root + "/" + f) 此处定义的size无法在commonfiles进行比较. (A,B在各自的循环里面)

    # print(afiles, bfiles)

    # 去掉 afiles 中文件名的 apath (拿A,B相同的路径\文件名,做成集合,去找交集)
    apathlen = len(apath)
    aafiles = []
    for f in afiles:
        aafiles.append(f[apathlen:])

    # 去掉 bfiles 中文件名的  bpath
    bpathlen = len(bpath)
    bbfiles = []
    for f in bfiles:
        bbfiles.append(f[bpathlen:])

    afiles = aafiles
    bfiles = bbfiles

    setA = set(afiles)
    setB = set(bfiles)
    # print('%$%'+str(len(setA)))
    # print('%%'+str(len(setB)))
    commonfiles = setA & setB  # 处理共有文件
    # print ("===============File with different size in '", apath, "' and '", bpath, "'===============")
    # 将结果输出到本地
    # with open(os.getcwd()+'diff.txt','w') as di:
    # di.write("===============File with different size in '", apath, "' and '", bpath, "'===============")
    # print(commonfiles)

    diff_info = []
    for f in sorted(commonfiles):
        a_file = os.path.join(apath + f)
        b_file = os.path.join(bpath + f)
        # print(apath, f, a_file, b_file)

        a_file_size = os.path.getsize(a_file)
        b_file_size = os.path.getsize(b_file)

        # return
        if a_file_size == b_file_size:  # 共有文件的大小比较
            # pass #print (f + "\t\t" + get_pretty_time(os.stat(a_file)) + "\t\t" + get_pretty_time(os.stat(b_file)))
            # 以下代码是处理大小一致，但是内容可能不一致的情况，比较 md5 需要的时间比较长
            a_file_md5 = get_file_md5(a_file)
            b_file_md5 = get_file_md5(b_file)
            if a_file_md5 == b_file_md5:
                continue
            else:
                # Git用<<<<<<<，=======，>>>>>>>标记出不同分支的内容。HEAD为当前所在分支的内容，也就是说现在master中的内容
                info = f'{"=" * 70}  文件MD5: {a_file_md5} != {b_file_md5}\n{f}\n\n'
                # "文件名=%s    MD5不同，文件 A:%s   !=  文件 B:%s" % (f, a_file_md5, b_file_md5)
            # print(os.getcwd())

        else:
            info = f'{"=" * 70}  文件大小: {a_file_size} != {b_file_size}\n{f}\n\n'

        # 只处理指定后缀的内容差异
        if os.path.splitext(a_file)[1].lower() in diff_ext:
            with open(a_file, 'r', encoding='utf-8') as f_in:
                AText = f_in.read()
            with open(b_file, 'r', encoding='utf-8') as f_in:
                BText = f_in.read()
            differ = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
            diff = differ.compare(
                AText.splitlines(keepends=True), BText.splitlines(keepends=True)  # keepends 包含换行符
            )
            diff = [d for d in diff if d.startswith('+') or d.startswith('-')]
            # print(''.join(diff))
            info += ''.join(diff)
            # if len(list(diff)) < 100:
            #     print(''.join(diff))
            #     exit()

        # 文件不同的时候处理
        diff_info.append(info)
        print(info)

    diff_file = os.path.join(out_dir, 'diff.txt')
    if os.path.exists(diff_file):
        os.remove(diff_file)
    if diff_info:
        with open(diff_file, 'a', encoding='utf-8') as di:
            di.write('\n'.join(diff_info))
    else:
        if diff_ext:
            print(f'文件夹中的 {diff_ext} 后缀名文件没有差异')

    # 处理仅出现在一个目录中的文件
    onlyFiles = setA ^ setB
    aonlyFiles = []
    bonlyFiles = []
    for of in onlyFiles:
        if of in afiles:
            aonlyFiles.append(of)
        elif of in bfiles:
            bonlyFiles.append(of)

    # print ("###################### EE resource ONLY ###########################")
    # print ("#only files in ", apath)
    a_only_file = os.path.join(out_dir, os.path.basename(apath) + ' only.txt')
    b_only_file = os.path.join(out_dir, os.path.basename(bpath) + ' only.txt')
    if os.path.exists(a_only_file):
        os.remove(a_only_file)
    if os.path.exists(b_only_file):
        os.remove(b_only_file)

    aonly_count = len(aonlyFiles)
    bonly_count = len(bonlyFiles)

    if aonly_count:
        with open(a_only_file, 'a') as a:
            for of in sorted(aonlyFiles):
                a.write(of + '\n')
                # a.write(apath + of + '\n')

        # print (of)
    # print ("*"*20+"SVN ONLY+"+"*"*20)
    # print ("#only files in ", bpath)

    if bonly_count:
        with open(b_only_file, 'a') as b:
            for of in sorted(bonlyFiles):
                b.write(of + '\n')
                # b.write(bpath + of + '\n')
            # print (of)

    print(apath, 'only files numbers:', aonly_count)
    print(bpath, 'only files numbers:', bonly_count)


def get_compound_file_binary(file):
    """
    获取复合文件二进制格式文件中的数据

    Compound File Binary Format Files
    https://stackoverflow.com/questions/12705527/reading-excel-files-with-xlrd
    """
    try:
        import olefile
        with open(file, 'rb') as f:
            if str(file).endswith('.xls'):
                ole = olefile.OleFileIO(f)
                # print(ole.listdir())
                if ole.exists('Workbook'):
                    d = ole.openstream('Workbook')
                    return d.read()
            return f.read()
    except ImportError as e:
        print(Fore.RED + "注：找不到 olefile，请安装它: pip install olefile", Style.RESET_ALL)
        pass


def synch_git_files(src, dst, remove_src=False):
    count = 0
    remove_count = 0

    # 先把修改同步到dst文件夹
    for dir_path, dir_names, file_names in os.walk(src):
        dir_name_list = dir_path.split(os.path.sep)
        if '.git' in dir_name_list or '-' in dir_name_list:
            continue
        # print(dir_name_list)

        for _file_name in file_names:
            # if _file_name.startswith('.'):
            #     continue

            is_copy = False
            info = ''
            src_file = os.path.join(dir_path, _file_name)
            dst_file = src_file.replace(src, dst)
            if os.path.exists(dst_file):
                src_hash = get_file_hash(src_file)
                dst_hash = get_file_hash(dst_file)
                if src_hash != dst_hash:
                    is_copy = True
                    info = f'文件哈希不同  {src_hash} {dst_hash} {src_file} {dst_file}'
            else:
                is_copy = True
                info = f'没有找到文件 {dst_file}'
            if is_copy:
                count += 1
                print(is_copy, info, )

                dst_dir = os.path.dirname(dst_file)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copy(src_file, dst_file)

    # 删除目标文件夹多余的文件
    for dir_path, dir_names, file_names in os.walk(dst):
        dir_name_list = dir_path.split(os.path.sep)
        if '.git' in dir_name_list or '-' in dir_name_list:
            continue
        # print(dir_name_list)

        for _file_name in file_names:
            # if _file_name.startswith('.'):
            #     continue

            is_remove = False
            info = ''
            dst_file = os.path.join(dir_path, _file_name)
            src_file = dst_file.replace(dst, src)

            if not os.path.exists(src_file):
                is_remove = True
                info = f'目的文件夹多的文件 {src_file}'

            if is_remove:
                print(is_remove, info, )
                if remove_src:
                    os.remove(src_file)
                remove_count += 1

    if remove_src:
        print(f'修改 {count} 删除 {remove_count}')
    else:
        print(f'修改 {count} 需要删除的文件 {remove_count}')


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
        print('json_read', e)
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
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_crc32)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_md5)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_text_md5)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=human_size)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_this_dir)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_this_dir_2)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_line_info)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=file_string_replace)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=exists_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=exists_file_to_bak)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_name)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=list_dir)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=from_dir_func)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=save_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=dir_compare)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=json_read)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=json_save)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()
    get_compound_file_binary('compound_file')
    doc()

    # 性能测试
    # from timeit import timeit
    # print(timeit('validate_title("\\fasdf/f:*?dasfdddddddddddddddddddddda<fasf>|")', 'from file import validate_title', number=1000000))
    # replace_invalid_filename_char 稍微快一点
    # print(timeit('replace_invalid_filename_char("\\fasdf/f:*?dasfdddddddddddddddddddddda<fasf>|")', 'from file import replace_invalid_filename_char', number=1000000))

    print('运行时间 %.2f 秒' % (time() - start_time))

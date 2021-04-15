# ---------------------------------------
#   程序：everything.py
#   版本：0.2
#   作者：lds
#   日期：2020-10-06
#   语言：Python 3.X
#   说明：Everything 搜索相关的函数集合

import os
import sys
import csv
import datetime
import warnings

try:
    from ctypes import windll, create_unicode_buffer, c_wchar_p, byref
except ImportError as e:
    warnings.warn(f'{e}, Linux 不能使用 ctypes，所以 Everything 不能运行！')

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

SORT_TYPE = {
    'EVERYTHING_SORT_NAME_ASCENDING': 1,
    'EVERYTHING_SORT_NAME_DESCENDING': 2,
    'EVERYTHING_SORT_PATH_ASCENDING': 3,
    'EVERYTHING_SORT_PATH_DESCENDING': 4,
    'EVERYTHING_SORT_SIZE_ASCENDING': 5,
    'EVERYTHING_SORT_SIZE_DESCENDING': 6,
    'EVERYTHING_SORT_EXTENSION_ASCENDING': 7,
    'EVERYTHING_SORT_EXTENSION_DESCENDING': 8,
    'EVERYTHING_SORT_TYPE_NAME_ASCENDING': 9,
    'EVERYTHING_SORT_TYPE_NAME_DESCENDING': 10,
    'EVERYTHING_SORT_DATE_CREATED_ASCENDING': 11,
    'EVERYTHING_SORT_DATE_CREATED_DESCENDING': 12,
    'EVERYTHING_SORT_DATE_MODIFIED_ASCENDING': 13,
    'EVERYTHING_SORT_DATE_MODIFIED_DESCENDING': 14,
    'EVERYTHING_SORT_ATTRIBUTES_ASCENDING': 15,
    'EVERYTHING_SORT_ATTRIBUTES_DESCENDING': 16,
    'EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING': 17,
    'EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING': 18,
    'EVERYTHING_SORT_RUN_COUNT_ASCENDING': 19,
    'EVERYTHING_SORT_RUN_COUNT_DESCENDING': 20,
    'EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING': 21,
    'EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING': 22,
    'EVERYTHING_SORT_DATE_ACCESSED_ASCENDING': 23,
    'EVERYTHING_SORT_DATE_ACCESSED_DESCENDING': 24,
    'EVERYTHING_SORT_DATE_RUN_ASCENDING': 25,
    'EVERYTHING_SORT_DATE_RUN_DESCENDING': 26,
}

EVERYTHING_ERROR = {
    0: '操作成功完成',
    1: '无法为搜索查询分配内存',
    2: 'IPC 不可用',
    3: '无法注册搜索查询窗口类',
    4: '无法创建搜索查询窗口',
    5: '无法创建搜索查询线程',
    6: '索引无效，索引必须大于或等于0且小于可见结果的数量',
    7: '呼叫无效',
}


class SearchError(Exception):
    """ 搜索错误"""
    pass


def reader_efu(efu_file, encoding='utf-8'):
    """
    读取 EFU 文件

    文件是包含文件名、大小、日期以及属性列表的逗号分隔值 (CSV) 文件

    header ['Filename', 'Size', 'Date Modified', 'Date Created', 'Attributes']
    """
    # 读取csv文件
    with open(efu_file, newline='', encoding=encoding) as f:
        reader = csv.reader(f)  # delimiter=':', quoting=csv.QUOTE_NONE

        iter_reader = iter(reader)
        header = next(iter_reader)  # fieldnames
        # print(header)
        yield header

        try:
            for row in iter_reader:
                # print(row)
                yield row
        except csv.Error as e:
            print(f'csv.Error file {efu_file}, line {reader.line_num}: {e}')
            return
        # else:
        #     print('读取完成')


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


def get_data_from_dir(file_dir):
    """
    从文件目录获取 efu 文件列表信息
    """
    yield ['Filename', 'Size', 'Date Modified', 'Date Created', 'Attributes']
    if os.path.isdir(file_dir):
        # print('\n处理路径：\n%s\n' % file_dir)
        for root, dirs, files in os.walk(file_dir):
            file_info = os.stat(root)
            # https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat

            try:
                st_mtime = datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto')
            except Exception as e:
                st_mtime = ''
                print('st_mtime 错误：', root, e)

            try:
                st_ctime = datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto')
            except Exception as e:
                st_ctime = ''
                print('st_ctime 错误：', root, e)

            rows = [root, '',
                    st_mtime,
                    st_ctime, 16]
            yield rows
            for _filename in files:
                if _filename.startswith('.'):
                    continue
                _file = os.path.join(root, _filename)
                file_info = os.stat(_file)

                try:
                    st_mtime = datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto')
                except Exception as e:
                    st_mtime = ''
                    print('st_mtime 错误：', root, e)

                try:
                    st_ctime = datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto')
                except Exception as e:
                    st_ctime = ''
                    print('st_ctime 错误：', root, e)

                # print('st_mtime', file_info.st_mtime, os.path.getatime(_file),
                #       datetime.datetime.fromtimestamp(file_info.st_mtime).strftime(str_time),
                #       datetime.datetime.fromtimestamp(file_info.st_mtime).isoformat(sep='T', timespec='auto'))
                # print('st_ctime', file_info.st_ctime, os.path.getctime(_file),
                #       datetime.datetime.fromtimestamp(file_info.st_ctime).strftime(str_time),
                #       datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat(sep='T', timespec='auto'))
                rows = [_file, file_info.st_size,
                        st_mtime,
                        st_ctime, 0]
                yield rows


def create_efu(file_dir, efu_file=None, encoding='utf-8'):
    if efu_file is None:
        efu_file = f'{os.path.basename(file_dir)}.efu'
    writer_efu(efu_file, get_data_from_dir(file_dir), encoding=encoding)
    return efu_file


class Everything:
    """
    Everything SDK
    http://www.voidtools.com/support/everything/sdk/
    """

    def __init__(self, everything_dll):
        self.dll = windll.LoadLibrary(everything_dll)
        self.buffer = create_unicode_buffer(256)

    def search(self, text, sort=None, max_count=None):
        """
        搜索文件

        代码参考：
        http://www.oschina.net/question/17793_38696?sort=time
        """

        self.dll.Everything_SetSearchW(c_wchar_p(text))
        # 设置搜索结果排序
        if sort is not None and sort in SORT_TYPE:
            self.dll.Everything_SetSort(SORT_TYPE[sort])
        # 获取结果的最大数量
        if isinstance(max_count, int):
            self.dll.Everything_SetMax(max_count)

        self.dll.Everything_QueryW(True)

        last_error = self.dll.Everything_GetLastError()
        if last_error == 0:
            count = self.dll.Everything_GetNumResults()
            if count == 0:
                print("没有找到文件！", text)

            for index in range(count):
                self.dll.Everything_GetResultFullPathNameW(index, byref(self.buffer), len(self.buffer))
                # print(self.buffer.value.encode("gbk"))
                yield self.buffer.value
        else:
            raise SearchError(f'搜索失败：错误代码 {last_error}, 错误信息：{EVERYTHING_ERROR.get(last_error, None)}')

    def close(self):
        del self.dll
        del self.buffer


if __name__ == "__main__":
    from ilds.time import Timer

    t1 = Timer()

    # print(reader_efu(r"file.efu", encoding='utf-8'))
    # create_efu(r'file_dir', efu_file=None, encoding='utf-8')

    e = Everything(r"D:\my\测试用户\lib\everything\Everything32.dll")
    if len(sys.argv) > 1:
        search_text = sys.argv[1]
    else:
        # print("参数错误！")
        search_text = r'"c:\program files\"'

    print("开始搜索：%s\n---------------------------------" % search_text)
    print(list(e.search(search_text)))
    print(list(e.search('测试用户')))
    e.close()

    t1.running_time()

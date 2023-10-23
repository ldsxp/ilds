# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：match_data.py
#   版本：0.2
#   作者：lds
#   日期：2023-04-27
#   语言：Python 3.X
#   说明：使用 pandas 匹配的函数集合
# ---------------------------------------


import os
from collections import OrderedDict

"""
我们为了在服务器使用匹配结果，大部分函数返回结果是：{'infos': infos, 'data': data} 或者 {'infos': infos, 'data': df}
"""

try:
    import pandas
except ImportError as e:
    raise ImportError("导入 pandas 失败，如果没有安装，请安装它: pip install pandas")

from .util import cleaning_str, cleaning_digital
from .pd import get_columns_index


def get_exists_dup(array_like, *args):
    """
    获取用来检查重复的内容
    """
    exists_dup = ''.join([array_like[k].strip() for k in args])
    return cleaning_str(exists_dup)


def get_digital_dup(array_like, *args):
    """
    获取用来检查的数字内容
    """
    exists_dup = str(array_like[args[0]]).strip()
    try:
        return str(int(exists_dup.split('.')[0]))
    except Exception as e:
        print(f'{exists_dup} {e}')


def cleaning_data(df, is_digital=False, dropna_subset=None, exists_subset=None, astype_str_list=None,
                  multiple_results=False, replace_columns=None):
    """
    清理检查添加中的空白内容和多余符号

    :param df:
    :param is_digital: 是普通模式还是数字模式，数字模式的时候不转为内容为字符串，不清理无用符号，把内容转换为数字（如果是浮点，去掉小数点，如果不能转换，保留原始内容）
    :param dropna_subset: 需要清理的列表
    :param exists_subset: 需要检查重复的条件，也是
    :param astype_str_list: 需要转换为字符串的表格（列）
    :param multiple_results: 填充匹配到的多个结果
    :param replace_columns: 要填充的内容
    :return: 处理过的 df
    """
    infos = []

    # print('cleaning_data', is_digital, dropna_subset, exists_subset, astype_str_list, multiple_results, replace_columns)

    # 清理需要检查数据中的空白内容
    if dropna_subset is not None:
        old_count = len(df)
        df = df.dropna(how='all', subset=dropna_subset)
        info = f'cleaning_data {dropna_subset} 删除空白内容：{old_count - len(df)} 行'
        print(info)
        infos.append(info)

    # print('填充数据表中空值')
    df = df.fillna(value='')

    if is_digital:
        if exists_subset is not None:
            df['检查重复'] = df.apply(get_digital_dup, axis=1, args=exists_subset)
        # raise ValueError('检查重复')
    else:
        # 转换表格内容为字符串
        if isinstance(astype_str_list, list):
            for astype_str in astype_str_list:
                df[astype_str] = df[astype_str].astype(str)
                print(df[astype_str].astype(str))
        # 处理用来检查重复的字段 清理无用符号
        if exists_subset is not None:
            df['检查重复'] = df.apply(get_exists_dup, axis=1, args=exists_subset)

    # print('替换数据')
    if multiple_results and replace_columns is not None:
        # 用来保存重复的数据，后面我们合并她
        replace_dict = {}
        # 要替换的列
        check_columns_index = get_columns_index(df, replace_columns)
        check_index = get_columns_index(df, ['检查重复'])[0]
        for i, df_line in enumerate(df.values):
            key = df_line[check_index]
            if key in replace_dict:
                df_line_1 = replace_dict[key]
                # if i < 500:
                #     print(df_line_1, )
                for index in check_columns_index:
                    df_line_1[index] = f"{df_line_1[index]}|{df_line[index]}"
                # if i < 500:
                #     print(df_line_1)
            else:
                replace_dict[key] = df_line

        # print(df)
        df = pandas.DataFrame(replace_dict.values(), columns=df.columns)
        # print(df)

    # print(infos)

    return {'infos': infos, 'data': df}


def df_search(_df, column, keyword, case=True, flags=0, na=None, regex=True):
    """
    在 DataFrame 中搜索

    实现依靠 re.search，也可以是用 re.match

    @param _df: 要搜索的 pandas.DataFrame
    @param column: 要搜索的列名
    @param keyword: str 要搜索的字符或正则表达式
    @param case: 默认为 True，如果为 True 则区分大小写
    @param flags: 默认0（无标志），标志将传递到RE模块，例如 re.IGNORECASE
    @param na: 缺失值的可选填充值
    @param regex: 默认为 True，如果为 True，则使用正则表达式。 如果是 False 则将视为字面字符串
    @return: 搜索到的 pandas.DataFrame

    # 可以看看
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html?highlight=contains
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.match.html#pandas.Series.str.match
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.startswith.html#pandas.Series.str.startswith
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.endswith.html#pandas.Series.str.endswith
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.fullmatch.html#pandas.Series.str.fullmatch
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html

    ## 例子
    # 创建一个 DataFrame
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'age': [25, 30, 35, 40, 45],
        'gender': ['F', 'M', 'M', 'M', 'F']
    }
    df = pd.DataFrame(data)

    # 进行搜索
    result = df_search(df, 'name', 'a', case=True, flags=0, na=None, regex=True)
    print(result)

    # 显示 DataFrame 的索引号和内容
    for index, row in result.iterrows():
        print(f'索引({type(index)}): {index}, 数据({type(row)}): {row}')
    for index, row in zip(result.index, result.values):
        print(f'索引({type(index)}): {index}, 数据({type(row)}): {row}')

    # 在 pandas 中，可以使用比较运算符（如 >, <, ==, != 等）或 isin() 方法搜索指定的数字。
    print(df[df['age'] == 25])
    # 如果要搜索多个数字，可以使用 isin() 方法。例如，以下代码搜索 age 列中值为 25 或 30 的所有行：
    print(df[df['age'].isin([25, 30])])
    """
    return _df[_df[column].str.contains(keyword, case=case, flags=flags, na=na, regex=regex)]


def match_data(df1, df2, check_columns, replace_columns, is_digital):
    """
    匹配数据并填充匹配到的数据
    """

    infos = []

    # 填充数据表中空值
    df2 = df2.fillna(value='')

    # 要检查的列
    check_columns_index = get_columns_index(df2, check_columns)

    replace_count = 0

    # 设置要填充的列的值
    for replace_column in replace_columns:
        if replace_column not in df2.columns:
            df2[replace_column] = ''

    # 要填充的数据
    replace_columns_index = get_columns_index(df1, replace_columns)
    info = f"填充的数据:{replace_columns}，填充的数据索引:{replace_columns_index}"
    print(info)
    infos.append(info)

    for i, df_line in enumerate(df2.values):
        # print(df_line)
        # print(''.join([df_line[k] for k in check_columns_index]))
        # 获取需要检查的内容
        try:
            if is_digital:
                ch = get_digital_dup(df_line, *check_columns_index)
            else:
                ch = get_exists_dup(df_line, *check_columns_index)
        except Exception as e:
            # print([df_line[k] for k in check_columns_index])
            raise ValueError('%s %s' % ([str(df_line[k]) for k in check_columns_index], e))

        # if len(df1[df1['检查重复'].isin([ch])]) > 1:
        #     print(df1[df1['检查重复'].isin([ch])])
        #     # print(get_exists_dup(df_line))

        # if i < 200000000:
        replace_dict = {}
        # if len(df1[df1['检查重复'].isin([ch])]):
        # 找到重复内容
        for df_neirong in df1[df1['检查重复'].isin([ch])].values:
            # print(df_neirong)
            # 填充重复内容
            for columns_i in range(len(replace_columns)):
                # print(df_neirong[replace_columns_index[columns_i]])
                # 把找到的歌曲放在字典里面
                neirong = df_neirong[replace_columns_index[columns_i]]
                replace_column = replace_columns[columns_i]
                # if neirong:
                if replace_column in replace_dict and neirong != replace_dict[replace_column]:
                    info = f'重复: {neirong}'
                    print(info)
                    infos.append(info)
                else:
                    replace_dict[replace_column] = neirong
                    # print(f'匹配：{ch} ------------- 找到 {replace_column}: {neirong}')
        # 处理找到的结果
        # print(df_line)
        # if replace_dict:
        #     print('找到内容',df_line)
        # 替换找到的内容到表格
        for k, v in replace_dict.items():
            df2.iloc[i, df2.columns.get_loc(k)] = v
            replace_count += 1

    # print(str(df2.values[0][0]))
    # print(''.join([df2.values[0][k] for k in check_columns_index]))
    # print(df1[df1['检查重复'].isin([get_exists_dup(df2.values[0])])])
    # df1.iloc[0, df.columns.get_loc('表演者2')] = 5

    # print(strstrip(''.join([df2.values[0][k] for k in check_columns_index])))
    # print(df2.values[0])

    info = f'行数: {len(df2.values)}，填充: {replace_count}'
    print(info)
    infos.append(info)

    return {'infos': infos, 'data': df2}


def add_duplicate_tags(df1, df2, check_columns, tags_title="重复", tags_list=None, is_digital=False):
    """
    匹配数据并添加重复标记
    """

    infos = []

    if tags_list is None:
        tags_list = ['是', '否']  # True, False

    # 要检查的列
    check_columns_index = get_columns_index(df2, check_columns)

    chongfu_count = 0

    df2[tags_title] = tags_list[1]
    chongfu_col = df2.columns.get_loc(tags_title)
    # print(len(df2.columns))

    for i, df_line in enumerate(df2.values):
        # print(df_line)
        # print(''.join([df_line[k] for k in check_columns_index]))
        try:
            if is_digital:
                ch = cleaning_digital(''.join([str(df_line[k]) for k in check_columns_index]))
            else:
                ch = cleaning_str(''.join([df_line[k] for k in check_columns_index]))
        except Exception as e:
            # print([df_line[k] for k in check_columns_index])
            raise ValueError('%s %s' % ([df_line[k] for k in check_columns_index], e))

        # if len(df1[df1['检查重复'].isin([ch])]) > 1:
        #     print(df1[df1['检查重复'].isin([ch])])
        #     # print(get_exists_dup(df_line))

        # if i < 200000000:
        replace_dict = {}
        if len(df1[df1['检查重复'].isin([ch])]):
            # 标记重复内容
            # print(len(df2.columns))
            df2.iloc[i, chongfu_col] = tags_list[0]
            chongfu_count += 1

    # print(str(df2.values[0][0]))
    # print(''.join([df2.values[0][k] for k in check_columns_index]))
    # print(df1[df1['检查重复'].isin([get_exists_dup(df2.values[0])])])
    # df1.iloc[0, df.columns.get_loc('表演者2')] = 5

    # print(strstrip(''.join([df2.values[0][k] for k in check_columns_index])))
    # print(df2.values[0])

    info = f'行数：{len(df2.values)}, 重复: {chongfu_count}'
    print(info)
    infos.append(info)

    return {'infos': infos, 'data': df2}


def fill_in_the_matched_data(df, data, check_columns, replace_columns, is_digital=False, multiple_results=False):
    """
    填充匹配到的数据

    :param df: 文件 1
    :param data: 文件 2（支持多个表的数据）
    :param check_columns: 检查条件
    :param replace_columns: 要填充的内容
    :param is_digital: 数字版
    :param multiple_results: 填充匹配到的多个结果
    :return:
    """

    infos = []

    r = cleaning_data(df, is_digital=is_digital, dropna_subset=check_columns, exists_subset=check_columns,
                      astype_str_list=check_columns, multiple_results=multiple_results,
                      replace_columns=replace_columns)
    df = r['data']
    info = r['infos']
    print(info)
    infos.extend(info)

    # print(df.columns)
    print('填充匹配到的数据', '-' * 70)
    info = f'文件A 表薄行数: {len(df)}'
    print(info)
    infos.append(info)

    # 处理多表文件（匹配并替换内容）
    for sheet_name, df_data in data.items():
        r = cleaning_data(df_data, is_digital=is_digital, dropna_subset=check_columns,
                          astype_str_list=check_columns, replace_columns=None)
        df_data = r['data']
        info = r['infos']
        print(info)
        infos.extend(info)

        # # 清理没有歌曲名和作者的行
        # df_data = df_data.dropna(how='all', subset = ['歌曲名称','表演者'])
        # # 转换表格为字符串
        # df_data["歌曲名称"] = df_data["歌曲名称"].astype(str)

        # 匹配两个文件中的数据 并把第一个文件内容填充到第二个文件
        info = f'匹配表薄: {sheet_name}，行数: {len(df_data)}'
        print(info)
        infos.append(info)
        r = match_data(df, df_data, check_columns, replace_columns, is_digital=is_digital)
        infos.extend(r['infos'])
        data[sheet_name] = r['data']

    return {'infos': infos, 'data': data}


def mark_duplicate(df, data, check_columns, is_digital=False):
    """
    标记重复
    """

    infos = []

    r = cleaning_data(df, is_digital=is_digital, dropna_subset=check_columns, exists_subset=check_columns,
                      astype_str_list=check_columns, replace_columns=None)
    infos.extend(r['infos'])
    df = r['data']
    # print(df.columns)

    # 处理多表文件（匹配并替换内容）
    for sheet_name, df_data in data.items():
        r = cleaning_data(df_data, is_digital=is_digital, dropna_subset=check_columns,
                          astype_str_list=check_columns, replace_columns=None)
        infos.extend(r['infos'])
        df_data = r['data']

        # 匹配两个文件中的数据 并把第一个文件内容存在第二个文件的数据标记重复
        print('标记重复数据', '-' * 70)
        info = f'表薄: {sheet_name}，行数: {len(df_data)}'
        print(info)
        infos.append(info)
        # 默认标记重复
        r = add_duplicate_tags(df, df_data, check_columns=check_columns, is_digital=is_digital)
        infos.extend(r['infos'])
        data[sheet_name] = r['data']

    return {'infos': infos, 'data': data}


def check_duplicate_content(data, check_columns, keep='first', is_duplicate=True, is_digital=False):
    """
    标记单个文件中的重复行

    例子
    data = get_excel_file_to_dfs(excel_file2)
    check_columns = ['歌曲名称', '表演者', '词作者', '曲作者', '内部采购子合同编号']  # , '专辑名称', '厂牌名称'
    data = check_duplicate_content(data, check_columns, keep='first', is_duplicate=True)

    :param data: 检查重复数据
    :param check_columns: 需要检查重复的字段列表
    :param keep: 'first'：除了第一个之外，将重复标记为“True”(duplicated 默认)，'last'：除了最后一个之外，Mark重复为“True”，False ：将所有重复项标记为“True”
    :param is_duplicate: 是否保留判断重复的列
    :param is_digital:
    :return:
    """

    infos = []

    print('开始标记单文件重复内容...')

    for sheet_name, df_data in data.items():
        # df_data['重复'] = df_data.duplicated()
        # df_data['重复'] = df_data.duplicated(keep=False) # 不太好用{‘first’, ‘last’, False}, default ‘first’
        # 还是需要清理，因为文本经常会有多余字符
        # continue # 不清理符号 直接检查重复内容
        r = cleaning_data(df_data, is_digital=is_digital, dropna_subset=check_columns,
                          exists_subset=check_columns, astype_str_list=check_columns, replace_columns=None)
        df_data = r['data']
        infos.extend(r['infos'])
        # print(df_data.columns)
        df_data['重复'] = df_data.duplicated(['检查重复'], keep=keep)  # 指定特定的列，默认所有列
        print(df_data.columns)

        if is_duplicate:
            data[sheet_name] = df_data
        else:
            data[sheet_name] = df_data.drop(columns=['检查重复'])  # 删除(检查重复)列

        # 删除重复行 drop_duplicates
        # if is_drop_duplicates:
        #     data[sheet_name] = df_data.drop_duplicates(check_columns)

    return {'infos': infos, 'data': data}


def generated_file_path(excel_file, check_columns=None, replace_columns=None):
    """生成文件名字"""
    neme = ''
    if check_columns:
        check = '、'.join(check_columns)
        neme += f' 匹配（{check}）'

    if replace_columns:
        replace = '、'.join(replace_columns)
        neme += f' 填充（{replace}）'
    else:
        neme += ' 标记重复'

    i = 1
    file_path, _ = os.path.splitext(excel_file)
    while True:
        file = file_path + neme + ' 结果 {0:0>2}'.format(i) + '.xlsx'
        if not os.path.exists(file):
            return file
        i += 1

import pandas as pd


def get_columns_index(df, columns):
    """获取列名称在 DataFrame 中的索引"""
    if isinstance(columns, str):
        columns = [columns]
    columns_index = []
    for col in columns:
        columns_index.append(df.columns.get_loc(col))
    # print('columns_index', columns_index)
    return columns_index


def aggregate_data(df, group_columns, sum_columns):
    """
    根据用户指定的列进行分组和汇总 DataFrame

    参数:
        df (DataFrame): 输入 Pandas DataFrame
        group_columns (list of str): 需要分组的列名列表
        sum_columns (list of str): 需要汇总的列名列表

    返回:
        DataFrame: 经过分组和汇总的数据
    """

    # 检查输入列是否在DataFrame中
    missing_cols = set(group_columns + sum_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"以下的列不存在，不能分组和汇总: {missing_cols}")

    # 将需要汇总的列中的缺失值填充为0
    # df[sum_columns] = df[sum_columns].fillna(0) # 我们在遇到None列的时候，这种方式会失败
    for column in sum_columns:
        try:
            df[column] = df[column].fillna(0)
        except Exception as e:
            print(f'汇总列 “{column}” 填充数据失败，转为浮点数重新填充。错误信息：{e}')
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df[column] = df[column].fillna(0)
    # 填充缺失值为空字符串
    df[group_columns] = df[group_columns].fillna('')

    # 创建聚合字典并进行分组汇总
    agg_dict = {column: 'sum' for column in sum_columns}
    return df.groupby(group_columns, as_index=False).agg(agg_dict)


def add_sorted_sequence_number(df, sort_column, ascending=False, sort_name='排序序号'):
    """
    根据指定列的值生成排序序号，并将序号合并回原始DataFrame中

    @param df: 输入的DataFrame
    @param sort_column: 用于排序序号的列名
    @param ascending: 排序方式 True 表示升序排列，从小到大；False表示降序排列，从大到小（默认）
    @param sort_name: 排序列的名字
    @return: 添加了排序序号的 pd.DataFrame
    """
    # 将指定列转换为数值类型，无法转换的值变为 NaN
    df[sort_column] = pd.to_numeric(df[sort_column], errors='coerce')

    # 创建一个排序后的DataFrame
    df_sorted = df[[sort_column]].sort_values(by=sort_column, ascending=ascending).reset_index()

    # 添加序号列
    df_sorted[sort_name] = range(1, len(df_sorted) + 1)

    # 合并'排序序号'回原始DataFrame
    df = df.merge(df_sorted[['index', sort_name]], left_index=True, right_on='index').drop(columns=['index'])

    return df


def get_excel_max_rows_percentage(dataframe):
    """
    计算 DataFrame 数据占 Excel 最大行数的百分比
    """
    # Excel 2007及之后版本的最大行数
    excel_max_rows = 1048576

    # 获取 DataFrame 的行数
    dataframe_rows = len(dataframe)

    # 计算百分比
    percentage = (dataframe_rows / excel_max_rows) * 100

    # print(f'占 Excel 的 {percentage:.2f}%')

    return percentage


def filter_and_pivot(df, filter_ids, filter_dates, row_label='数据日期', column_label='中央曲库ID', aggregate_column='CP分成收入', agg_func='sum', fill_value=None):
    """
    根据给定的中央曲库ID列表和数据日期列表过滤数据，并生成透视表。

    参数：
    df: pandas DataFrame，包含原始数据
    filter_ids: str，要筛选的内容
    filter_dates: str，要筛选的内容2
    row_label: str，行索引列名
    column_label: str，列索引列名
    aggregate_column: str，要计算的列名
    agg_func: 聚合函数
    fill_value: 填充缺失值

    返回：
    pandas DataFrame，透视表
    """

    print(f'{"-" * 50}')
    print('筛选需要的数据')
    print(f'列:{list(df.columns)}')
    df_len = len(df)
    df_total = df[aggregate_column].sum()
    print(f'数据行数 {df_len} 合计: {df_total}')

    # 过滤出指定的column_label(默认：中央曲库ID)和row_label(默认：数据日期)的数据
    filtered_df = df[(df[column_label].isin(filter_ids)) & (df[row_label].isin(filter_dates))]

    if fill_value is None:
        # 创建透视表
        pivot_table = filtered_df.pivot_table(index=row_label, columns=column_label, values=aggregate_column, aggfunc=agg_func, margins=True)
    else:
        # 创建透视表，并填充缺失值为 0
        pivot_table = filtered_df.pivot_table(index=row_label, columns=column_label, values=aggregate_column, aggfunc=agg_func, fill_value=fill_value, margins=True)

    # print(pivot_table.head())
    # 计算合计，并删除合计列
    # 保存合计行和列
    total_sum_a = pivot_table.loc['All', 'All']
    print(f'计算合计A：{total_sum_a}')
    total_sum_b = pivot_table.loc['All'].drop('All').sum()
    print(f'计算合计B：{total_sum_b}')
    # 计算占全部数据的百分比
    print(f'占比：{round((total_sum_a / df_total) * 100, 2)}%')
    # 删除合计行和列
    pivot_table = pivot_table.drop(index='All', columns='All')

    # 转置数据框使列为values(默认：中央曲库ID)
    result = pivot_table.T

    print(f'找到：{len(result)} / {len(filter_ids)} = {round((len(result) / len(filter_ids)) * 100, 2)}%')
    print(f'{"-" * 50}')

    return {'sum': total_sum_a, 'df': result}

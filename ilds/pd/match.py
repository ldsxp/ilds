import pandas as pd

OPERATOR_MAP = {
    'exact': '精确匹配',
    'iexact': '忽略大小写匹配',
    'contains': '包含',
    'icontains': '忽略大小写包含'
}


def match_dataframe(df, conditions):
    """
    从Pandas数据中匹配满足特定条件的行

    :param df: 输入的 pandas 数据
    :param conditions: 字典列表，其中每个字典包含 field、operator（'exact', 'iexact', 'contains', 'icontains' 等）和比较的value。
                       可以选择添加 'convert_to_numeric': True 来尝试将字段转换为数字进行匹配。
    :return: 满足条件的过滤后的数据
    """
    # 初始条件为全True的布尔Series
    match_series = pd.Series([True] * len(df))

    # 根据条件过滤数据
    for condition in conditions:
        field = condition['field']
        operator = condition['operator']
        value = condition['value']
        convert_to_numeric = condition.get('convert_to_numeric', False)

        if convert_to_numeric:
            # 尝试将字段和值转换为数字
            df[field] = pd.to_numeric(df[field], errors='coerce')
            try:
                value = float(value)
            except ValueError:
                raise ValueError(f"值 {value} 不能转换为用于数字比较的浮点数")

            # 对数字进行匹配
            if operator == 'exact':
                match_series &= (df[field] == value)
            else:
                raise ValueError(f"数字的匹配条件不支持: {OPERATOR_MAP.get(operator, operator)}")
        else:
            # 字符串类型匹配，需要确保字段是字符串类型
            if not pd.api.types.is_string_dtype(df[field]):
                df[field] = df[field].astype(str)
                print(f'{field} 内容不是字符串', pd.api.types.is_string_dtype(df[field]))

            if operator == 'exact':
                match_series &= (df[field] == str(value))
            elif operator == 'iexact':
                match_series &= df[field].str.lower() == str(value).lower()
            elif operator == 'contains':
                match_series &= df[field].str.contains(value, na=False)
            elif operator == 'icontains':
                match_series &= df[field].str.contains(value, case=False, na=False)
            else:
                raise ValueError(f"匹配条件不支持: {OPERATOR_MAP.get(operator, operator)}")

    return df[match_series]


def 示例用法():
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'city': ['New York', 'Los Angeles', 'New York2', 'Chicago']
    }

    df = pd.DataFrame(data)

    conditions = [
        # {'field': 'city', 'operator': 'exact', 'value': 'New York'},
        # {'field': 'name', 'operator': 'icontains', 'value': 'A'},
        {'field': 'age', 'operator': 'exact', 'value': '30.0', 'convert_to_numeric': True, },
    ]

    result_df = match_dataframe(df, conditions)
    print(result_df)


if __name__ == '__main__':
    from ilds.time import Timer

    with Timer() as timer:
        ...
        示例用法()

import pandas as pd


def to_parquet(df, save_file):
    """
    保存为parquet数据函数，是为了记录使用方法
    """
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_parquet.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_parquet.html
    # 我们可以保存pyarrow数据，读取文件以后保存到当前文件夹的_d_文件夹中
    # df = pd.read_excel(file, dtype_backend='pyarrow')
    df.to_parquet(save_file)
    # restored_df = pd.read_parquet('data.parquet')


def write_to_excel(df, filename):
    """写入 DataFrame 数据到 Excel，一般我们会自定义这个函数"""
    import xlsxwriter

    workbook = xlsxwriter.Workbook(filename,
                                   # options={  # 全局设置
                                   #     'strings_to_numbers': True,  # str 类型数字转换为 int 数字
                                   #     'strings_to_urls': False,  # 自动识别超链接
                                   #     'constant_memory': False,  # 连续内存模式 (True 适用于大数据量输出)
                                   #     'default_format_properties': {
                                   #         # 'font_name': '微软雅黑',  # 字体. 默认值 "Arial"
                                   #         # 'font_size': 10,  # 字号. 默认值 11
                                   #         # 'bold': False,  # 字体加粗
                                   #         # 'border': 1,  # 单元格边框宽度. 默认值 0
                                   #         # 'align': 'left',  # 对齐方式
                                   #         # 'valign': 'vcenter',  # 垂直对齐方式
                                   #         # 'text_wrap': False,  # 单元格内是否自动换行
                                   #         # 'bg_color': 'white',
                                   #     },
                                   # }
                                   )

    workbook.set_properties({
        'title': f'标题',
        # 'subject': '',  # 主题
        'author': 'lds',
        # 'manager': '经理',
        # 'company': '公司',
        # 'category': '类别',
        # 'keywords': '关键字, 关键字, 关键字',
        # 'created': datetime.date(2018, 1, 1),  # 创建时间
        'comments': f'注释',
    })

    header_format = workbook.add_format({
        # 'bold': True,
        'text_wrap': True,
        # 'valign': 'top',
        # 'valign': 'vcenter',
        # 'align': 'center',
        'fg_color': '#c2cde0',
        'border': 1,

    })

    worksheet = workbook.add_worksheet(name=None)

    # 写入表头
    row = 0
    titles = list(df.columns)
    for col, header in enumerate(titles):
        worksheet.write(row, col, header, header_format)
        # 设置标题宽度
        worksheet.set_column(first_col=col, last_col=col, width=15, cell_format=None)

    row += 1

    for row_idx, row_data in df.iterrows():
        # print('Series 转换为字典', row_idx, row_data.to_dict())

        # 写入每一行的数据
        for col_idx, value in enumerate(row_data):
            worksheet.write(row, col_idx, value)

        row += 1

    workbook.close()


def writer_excel(obj, path, index=False, use_zip64=False):
    """
    保存 Excel 文件

    :param obj:
    :param path:
    :param index: 是否添加索引
    :param use_zip64:
    :return:
    """
    if isinstance(obj, dict):
        with pd.ExcelWriter(path) as writer:
            for sheet_name, df_data in obj.items():
                df_data.to_excel(writer, sheet_name=sheet_name, index=index)
            if use_zip64:
                writer.book.use_zip64()
    else:
        with pd.ExcelWriter(path) as writer:
            obj.to_excel(writer, sheet_name='Sheet1', index=index)
            if use_zip64:
                writer.book.use_zip64()

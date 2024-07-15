# 更改日志

此项目的所有显着更改都将记录在此文件中。

此项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [2024.7.15] - 2024-07-15
### Added
- ilds.pd.add_sorted_sequence_number 根据指定列的值生成排序序号，并将序号合并回原始DataFrame中

## [2024.5.8-2] - 2024-05-08
### Changed
- ilds.pd.merging_excel_file_data 添加一个严格模式的参数，限制要合并文件的标题

## [2024.5.8] - 2024-05-08
### Fixed
- ilds.pd.get_df_list 修复处理标题的错误

## [2024.5.7] - 2024-05-07
### Changed
- ilds.pd.merging_excel_sheet 添加一个严格模式的参数，限制要合并文件的标题

## [2024.5.6] - 2024-05-06
### Fixed
- ilds.pd.split_excel_sheet 修复保存目录为字符串路径的错误

## [2024.3.1] - 2024-03-01
### Added
- ilds.match_data 匹配检查重复的时候，提示重复的字段名

## [2024.1.18] - 2024-01-18
### Added
- ilds.spider 添加 get_jwt_token 登录以获取 JWT 令牌

## [2024.1.16] - 2024-01-16
### Fixed
- 修复 replace_invalid_filename_char 截断字符不能正确重命名的问题

## [2023.12.1-2] - 2023-12-01
### Changed
- pandas合并表数据的时候支持用 sheet_names 定义要合并的表

## [2023.12.1] - 2023-12-01
### Changed
- ilds.pd.get_df_list 支持自定义要读取的表

## [2023.10.23] - 2023-10-23
### Fixed
- ilds.match_data.match_data 修复匹配填充的时候，发现重复的匹配字段错误

## [2023.9.18-2] - 2023-09-18
### Fixed
- ilds.pd.split_excel_sheet 修复字典改成列表造成的错误
- 版本命名规则改为日期，因为 x.x.x 在 pypi 会造成困扰

## [2023.9.18] - 2023-09-18
### Changed
- ilds.pd.split_excel_sheet 优化Excel拆分
- 版本命名规则改为 x.x.x

## [2023.6.25-2] - 2023-06-25
### Changed
- ilds.pd.get_excel_data 支持读取表格状态参数 read_sheet_state

## [2023.6.25] - 2023-06-25
### Changed
- ilds.match_data.cleaning_data 打印处理信息

## [2023.5.16] - 2023-05-16
### Added
- ilds.file.get_excel_info 读取 Excel 信息
### Changed
- 把 json 中的 json_read 和 json_save 移动到 file

## [2023.4.27-2] - 2023-04-27
### Changed
- 把 ilds.pd.df_search 移动到 ilds.match_data.df_search

## [2023.4.27] - 2023-04-27
### Added
- ilds.pd.df_search 在 DataFrame 中搜索

## [2023.4.23] - 2023-04-23
### Changed
- ilds.pd.merging_excel_file_data 支持直接传入文件列表

## [2023.4.10] - 2023-04-10
### Changed
- ilds.pd.get_excel_data 返回表格的状态信息，这样我们可以选择是否处理隐藏表

## [2023.4.3] - 2023-04-03
### Changed
- ilds.pd.merging_excel_file_data 添加 get_files_function 参数，支持自定义获取文件的函数 

## [2023.2.21] - 2023-02-21
### Added
- ilds.file.synchr_git_files 同步git文件的修改
### Fixed
- ilds.file.get_file_hash 修复计算同一个文件，哈希不同的错误

## [2022.9.29] - 2022-09-29
### Added
- 添加一些要清理的符号

## [2022.9.7] - 2022-09-07
### Added
- 添加一个要清理的符号

## [2022.9.2] - 2022-09-02
### Added
- md5summer.create_md5 创建 md5summer md5 验证
- md5summer.checking_md5 检验文件的 md5 信息
- md5summer.save_tar 验证失败的文件保存到压缩包

## [2022.8.8] - 2022-08-08 未推送
### Changed
- ilds.pd.writer_excel 支持 use_zip64 参数

## [2022.8.8] - 2022-08-08
### Added
- ilds.pd.split_excel_sheet 拆分 Excel 表薄内容

## [2022.6.1] - 2022-06-01
### Fixed
- ilds.file.get_encoding 改为增量模式获取文件编码，让我们更有信心

## [0.1.100] - 2022-01-16
### Added
- ilds.util.check_out 检查标记退出的文件是否存在，存在的时候删除文件，并返回 True

## [0.1.99] - 2021-12-06
### Changed
- ilds.everything.create_efu 自动生成的文件名包含时间

## [0.1.98] - 2021-10-24
### Fixed
- ilds.match_data.fill_in_the_matched_data 修复信息列表问题

## [0.1.97] - 2021-09-30
### Added
- ilds.match_data.get_exists_dup 获取用来检查重复的内容
- ilds.match_data.get_digital_dup 获取用来检查的数字内容
- ilds.match_data.cleaning_data 清理检查添加中的空白内容和多余符号
- ilds.match_data.match_data 匹配数据并填充匹配到的数据
- ilds.match_data.add_duplicate_tags 匹配数据并添加重复标记
- ilds.match_data.fill_in_the_matched_data 填充匹配到的数据
- ilds.match_data.mark_duplicate 标记重复
- ilds.match_data.check_duplicate_content 标记单个文件中的重复行
- ilds.match_data.generated_file_path 生成文件名字
### Changed
- ilds.util.py.cleaning_str 因为在 pandas 不能传递参数，所以使用默认的 REPLACE_LIST
- ilds.util.py.get_excel_data 返回 columns 信息

## [0.1.96] - 2021-09-26
### Changed
- ilds.cmd 优化命令行选择

## [0.1.95] - 2021-07-22
### Changed
- ilds.pd.merging_excel_sheet 和 ilds.pd.merging_excel_file_data 支持 concat_kwargs 参数

## [0.1.94] - 2021-06-30
### Added
- ilds.file.get_hash 获取文件哈希信息

## [0.1.93] - 2021-04-15
### Fixed
- ilds.everything.Everything Linux 下不能使用 Everything，但可以使用其他函数

## [0.1.92] - 2021-03-05
### Changed
- ilds.time.Timer 添加开始时间显示

## [0.1.90] - 2021-01-21
### Fixed
- ilds.pd.merging_excel_sheet 合并 Excel 表薄内容

## [0.1.89] - 2021-01-07
### Fixed
- ilds.everything.get_data_from_dir 获取时间错误的时候只打印错误信息

## [0.1.88] - 2020-12-31
### Added
- ilds.file.get_hash_sums 添加参数 names，要获取的哈希名字列表

## [0.1.87] - 2020-12-05
### Added
- ilds.file 添加 get_hash_sums 和 get_file_hash 计算文件哈希

## [0.1.86] - 2020-10-12
### Changed
- ilds.everything 重命名 get_efu_data 为 get_data_from_dir
- ilds.everything reader_efu 返回生成器对象

## [0.1.85] - 2020-10-06
### Fixed
- ilds.everything 修复已知错误

## [0.1.84] - 2020-10-06
### Added
- ilds.everything 添加了 Everything 创建和读取文件列表的函数，搜索文件的 SDK 例子

## [0.1.83] - 2020-09-27
### Fixed
- ilds.file.get_compound_file_binary 处理非 olefile 文件发生错误

## [0.1.81] - 2020-09-14
### Changed
- ilds.time.Timer 时间显示改为人类可读

## [0.1.80] - 2020-08-29
### Changed
- ilds.file.check_filename_available 支持创建重复文件夹

## [0.1.79] - 2020-05-29
### Changed
- ilds.file.get_config 修改参数名为 file，支持 Pycharm 自动跳转到文件

## [0.1.78] - 2020-04-16
### Added
- ilds.pd.merging_excel_file_data 合并多个 Excel 文件内容
- ilds.pd.writer_excel 保存 Excel 文件

## [0.1.77] - 2020-04-15
### Added
- ilds.file.get_compound_file_binary 获取复合文件二进制格式文件中的数据

## [0.1.76] - 2020-03-06
### Changed
- ReadXlsx 读取文件的时候添加行数显示

## [0.1.75] - 2020-03-03
### Added
- ilds.file.check_filename_available 检查文件是否存在，如果已经存在，添加编号重命名
### Changed
- ilds.file.exist_or_makedir 添加弃用警告
- ilds.file.exists_file 添加弃用警告

## [0.1.74] - 2020-03-02
### Added
- ilds.util.time.time_str_to_second 把人类阅读的时间转换为秒，用来和 second_to_time_str 函数互相转换

## [0.1.73] - 2019-11-30
### Added
- ilds.util.admin.attrdict 可以用属性访问的字典

## [0.1.72] - 2019-11-04
### Changed
- 修改 django.model.confirm_db，在没有安装 wxpython 的时候，我们在命令行确认

## [0.1.70] - 2019-11-04
### Changed
- 修改 Windows 文件名时，删除更多非法字符，支持限制文件名最大长度

## [0.1.69] - 2019-10-30
### Added
- ilds.django.admin.ExportCsvMixin 支持设置导出文件的编码、自定义导出 ForeignKey 字段内容和排除导出字段

## [0.1.67] - 2019-10-24
### Fixed
- 修复获取 Django 模型使用的字典数据问题

## [0.1.66] - 2019-10-11
### Added
- ilds.mycsv 添加 csv_to_xls、csv_to_xlsx，转换 csv 文件为 Excel 文件

## [0.1.62] - 2019-09-07
### Added
- ilds.spider 添加 requests_retry_session，长链接会话，支持重试

## [0.1.60] - 2019-04-12
### Fixed
- 转换为 md 文件的编码错误

## [0.1.58] - 2019-06-13
### Added
- ilds.django.model 添加 calc_sum，计算 QuerySet 中指定字段的和

## [0.1.57] - 2019-06-12
### Added
- ilds.django.model 添加 TableData，转换 Eccel 数据为 Django 模型数据

## [0.1.56] - 2019-05-30
### Added
- ilds.django.admin 添加 ExportCsvMixin，导出 CSV 格式文件的动作

## [0.1.54] - 2019-05-27
### Added
- ilds.django.model 添加 get_model，通过库的名字或模型的名字获取模型

## [0.1.53] - 2019-05-26
### Added
- ilds.time 添加 Timer，计时器，可以当装饰器或者用 with 来对代码计时

## [0.1.52] - 2019-05-19
### Added
- ilds.util 添加 get_config，获取ini中的内容

## [0.1.51] - 2019-05-09
### Added
- ilds.lib.configobj 添加 ConfigObj，因为PyPI几年没有更新。文档：https://configobj.readthedocs.io，Github：https://github.com/DiffSK/configobj

## [0.1.50] - 2019-05-05
### Added
- ilds.django.import_export 添加 ModelData 根据 django 模型转换导入数据
- ilds.django.import_export 添加 dj_import_csv 导入csv文件到数据库
- ilds.django.import_export 添加 LdsExportCsv 写入数据到 csv 文件，支持自定义写入的表头，和要导出的字段
- ilds.django.import_export 添加 dj_export_csv 导出数据为csv文件

## [0.1.49] - 2019-04-26
### Added
- ilds.file 添加 human_size 以人类可读的格式返回大小

## [0.1.48] - 2019-04-12
### Changed
- 修正创建用户的时候，User 模型问题

## [0.1.46] - 2019-03-30
### Added
- ilds.file 添加 get_file_crc32 计算文件的 CRC32
- ilds.file 添加 dir_compare 比较两个目录的文件差异

## [0.1.45] - 2019-03-29
### Added
- ilds.time 添加 millisecond_to_timecode 毫秒转换为时间码字符串

## [0.1.44] - 2019-03-22
### Added
- 添加 CHANGELOG.md ，以后的更改日志保存到这里

### Changed
- 在 README.rst 中去掉更改日志
- 0.1.44 以前的更改日志放到 [CHANGELOG.rst](./CHANGELOG.rst) 中

### Fixed
- 全部更改日志在说明里面影响美观


# 更改日志

此项目的所有显着更改都将记录在此文件中。

此项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

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


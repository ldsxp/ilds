# 更改日志

此项目的所有显着更改都将记录在此文件中。

此项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

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


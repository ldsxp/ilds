from .excel import *


class ReadXlsx(ReadExcel):
    ...


warn(
    "excel_xlsx 已弃用，请使用 excel 代替",
    DeprecationWarning,
    stacklevel=2
)

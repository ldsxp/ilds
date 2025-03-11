# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：pd.py
#   版本：1.0
#   作者：lds
#   日期：2024-12-19
#   语言：Python 3.X
#   说明：pandas 常用的函数集合，TODO 添加一些小抄在这里！
# ---------------------------------------

from colorama import Fore, Back, Style

try:
    import pandas as pd
except ImportError as e:
    print(Fore.RED + "注：导入 pandas 失败，请安装它: pip install pandas", Style.RESET_ALL)
    pass

from .read import *
from .writer import *
from .excel import *
from .pd_util import *
from .match import *

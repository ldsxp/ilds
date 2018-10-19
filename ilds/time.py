# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：mytime.py
#   版本：0.3
#   作者：lds
#   日期：2018-10-19
#   语言：Python 3.X
#   说明：处理时间截的函数集合
# ---------------------------------------
import re
import time
from time import strptime
import datetime


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
    """
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
    """
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def now_to_timestamp(digits=10):
    """
    生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，
    输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
    """
    time_stamp = time.time()
    digits = 10 ** (digits -10)
    time_stamp = int(round(time_stamp*digits))
    return time_stamp


def timestamp_to_timestamp10(time_stamp):
    """
    将时间戳规范为10位时间戳
    """
    time_stamp = int (time_stamp* (10 ** (10-len(str(time_stamp)))))
    return time_stamp


def now_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    """
    将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
    """
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def date_style_transfomation(date, format_string1="%Y-%m-%d %H:%M:%S",format_string2="%Y-%m-%d %H-%M-%S"):
    """
    不同时间格式字符串的转换
    """
    time_array  = time.strptime(date, format_string1)
    str_date = time.strftime(format_string2, time_array)
    return str_date


def is_vaild_date(date):
    """
    判断是否是一个有效的日期字符串
    """
    try:
        if ":" in date:
            strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def form_time_to_year_mon_day(_time):
    """
    解析数字形式的日期 为 year-mon-day
    """
    time_str = str(_time)
    if len(time_str) == 6:
        year_s = time_str[:4]
        mon_s = time_str[4:6]
        # print((int(year_s), int(mon_s), int(day_s)))
        year_mon_day = '%s-%s-01'%(year_s, mon_s)
    elif len(time_str) == 8:
        year_s = time_str[:4]
        mon_s = time_str[4:6]
        day_s = time_str[6:8]
        # print((int(year_s), int(mon_s), int(day_s)))
        year_mon_day = '%s-%s-%s'%(year_s, mon_s, day_s)

    if is_vaild_date(year_mon_day):
        return year_mon_day
    else:
        raise ValueError(time_str + '不是有效的日期日期')


def date_from_str(date_str):
    """
    从字符串返回日期时间对象，格式为 YYYYMMDD 或（现在|今日）+ - ] [0-9]（天|周|月|年）？（S）
    Return a datetime object from a string in the format YYYYMMDD or
    (now|today)[+-][0-9](day|week|month|year)(s)?
    """
    today = datetime.date.today()
    if date_str in ('now', 'today'):
        return today
    if date_str == 'yesterday':
        return today - datetime.timedelta(days=1)
    match = re.match(r'(now|today)(?P<sign>[+-])(?P<time>\d+)(?P<unit>day|week|month|year)(s)?', date_str)
    if match is not None:
        sign = match.group('sign')
        time = int(match.group('time'))
        if sign == '-':
            time = -time
        unit = match.group('unit')
        # A bad approximation?
        if unit == 'month':
            unit = 'day'
            time *= 30
        elif unit == 'year':
            unit = 'day'
            time *= 365
        unit += 's'
        delta = datetime.timedelta(**{unit: time})
        return today + delta
    return datetime.datetime.strptime(date_str, '%Y%m%d').date()


def hyphenate_date(date_str):
    """
    将“YYYYMMDD”格式的日期转换为“YYYY-MM-DD”格式
    Convert a date in 'YYYYMMDD' format to 'YYYY-MM-DD' format
    """
    match = re.match(r'^(\d\d\d\d)(\d\d)(\d\d)$', date_str)
    if match is not None:
        return '-'.join(match.groups())
    else:
        return date_str

class DateRange(object):
    """
    表示两个日期之间的时间间隔
    Represents a time interval between two dates
    """

    def __init__(self, start=None, end=None):
        """start and end must be strings in the format accepted by date"""
        if start is not None:
            self.start = date_from_str(start)
        else:
            self.start = datetime.datetime.min.date()
        if end is not None:
            self.end = date_from_str(end)
        else:
            self.end = datetime.datetime.max.date()
        if self.start > self.end:
            raise ValueError('Date range: "%s" , the start date must be before the end date' % self)

    @classmethod
    def day(cls, day):
        """Returns a range that only contains the given day"""
        return cls(day, day)

    def __contains__(self, date):
        """Check if the date is in the range"""
        if not isinstance(date, datetime.date):
            date = date_from_str(date)
        return self.start <= date <= self.end

    def __str__(self):
        return '%s - %s' % (self.start.isoformat(), self.end.isoformat())


def srt_subtitles_timecode(seconds):
    """
    秒转换为时间字符串 01:02:03,000
    """
    return '%02d:%02d:%02d,%03d' % (seconds / 3600, (seconds % 3600) / 60, seconds % 60, (seconds % 1) * 1000)


def second_to_time_str(seconds):
    """
    秒转换为人类阅读的时间显示，用来显示已用时间
    例如：'1小时1分1.099秒'
    """
    time_str = ''
    hour = '%01d小时' % (seconds / 3600)
    minute = '%01d分' % ((seconds % 3600) / 60)

    if hour != '0小时':
        time_str += hour

    if minute != '0分':
        time_str += minute

    # seconds
    time_str += '%01d.%03d秒' % (seconds % 60, (seconds % 1) * 1000)

    return time_str


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=timestamp_to_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_to_timestamp)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=now_to_timestamp)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=timestamp_to_timestamp10)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=now_to_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_style_transfomation)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=is_vaild_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=form_time_to_year_mon_day)
    # youtube_dl\utils.py
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_from_str)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=hyphenate_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=DateRange)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=srt_subtitles_timecode)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=second_to_time_str)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

"""


Python处理时间和时间戳的内置模块就有time，和datetime两个，本文先说time模块。

关于时间戳的几个概念

时间戳，根据1970年1月1日00:00:00开始按秒计算的偏移量。
时间元组（struct_time），包含9个元素。 

time.struct_time(tm_year=2017, tm_mon=10, tm_mday=1, tm_hour=14, tm_min=21, tm_sec=57, tm_wday=6, tm_yday=274, tm_isdst=0) 

时间格式字符串，字符串形式的时间。
time模块与时间戳和时间相关的重要函数

time.time() 生成当前的时间戳，格式为10位整数的浮点数。
time.strftime()根据时间元组生成时间格式化字符串。
time.strptime()根据时间格式化字符串生成时间元组。time.strptime()与time.strftime()为互操作。
time.localtime()根据时间戳生成当前时区的时间元组。
time.mktime()根据时间元组生成时间戳。


实验

print(now_to_date())
print(timestamp_to_date(1506816572))
print(date_to_timestamp('2017-10-01 08:09:32'))
print(timestamp_to_timestamp10(1506816572546))
print(date_style_transfomation('2017-10-01 08:09:32'))

结果为

1506836224000
2017-10-01 13:37:04
2017-10-01 08:09:32
1506816572
1506816572
2017-10-01 08-09-32

"""
# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：time.py
#   版本：0.8.1
#   作者：lds
#   日期：2020-09-14
#   语言：Python 3.X
#   说明：处理时间截的函数集合
# ---------------------------------------
import re
import time
import datetime


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S", tz=None, is_str=True):
    """
    将 Unix 时间戳(10位)转换为时间字符串，默认为 2018-01-23 01:23:45 格式
    """
    d = datetime.datetime.fromtimestamp(float(time_stamp), tz)
    if is_str:
        date_str = d.strftime(format_string)
        return date_str
    return d


def timestamp13_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S", tz=None):
    """
    将 13 位时间戳转换为时间字符串，默认为 2018-01-23 01:23:45 格式
    """
    if len(str(time_stamp)) != 13:
        raise ValueError(time_stamp + '不是有效的 13 位 unix 时间戳')
    time_stamp = float(time_stamp) / 1000
    return timestamp_to_date(time_stamp, format_string, tz)


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转换为 Unix 时间戳(10位)，时间字符串默认为 2018-01-23 01:23:45 格式
    """
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def now_to_timestamp(digits=10):
    """
    生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为 10 位，
    输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
    """
    time_stamp = time.time()
    digits = 10 ** (digits - 10)
    time_stamp = int(round(time_stamp * digits))
    return time_stamp


def timestamp_to_timestamp10(time_stamp):
    """
    将时间戳规范为10位时间戳
    """
    time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
    return time_stamp


def now_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    """
    将当前时间转换为时间字符串，默认为 2018-01-23 01:23:45 格式
    """
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def get_now(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期和时间
    :return: 格式 2018-11-28 15:03:08
    """
    return datetime.datetime.now().strftime(fmt)


def get_now_date():
    """
    获取当前日期
    :return: 格式 2018-11-28
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_now_time():
    """
    获取当前时间
    :return: 格式 15:03:08
    """
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_past_date(amount, period='days', start_of_day=False):
    """
    获取过去的时间，可选择是否将时间设定为零点

    :param amount: 要回溯的数量，比如几天、几周或几个月前
    :param period: 时间类型，支持 'days', 'weeks', 或 'months'
    :param start_of_day: 布尔值，是否将时间设定为零点，默认不设定
    :return: 计算得到的日期和时间
    """
    from dateutil.relativedelta import relativedelta

    now = datetime.datetime.now()  # 获取当前的日期和时间

    if period == 'days':
        past_date = now - datetime.timedelta(days=amount)
    elif period == 'weeks':
        past_date = now - datetime.timedelta(weeks=amount)
    elif period == 'months':
        past_date = now - relativedelta(months=amount)
    else:
        raise ValueError("Invalid period. Use 'days', 'weeks', or 'months'.")

    if start_of_day:
        past_date = past_date.replace(hour=0, minute=0, second=0, microsecond=0)

    return past_date


def date_style_transfomation(date, format_string1="%Y-%m-%d %H:%M:%S", format_string2="%Y-%m-%d %H-%M-%S"):
    """
    不同时间格式字符串的转换
    """
    time_array = time.strptime(date, format_string1)
    str_date = time.strftime(format_string2, time_array)
    return str_date


def is_vaild_date(date):
    """
    判断是否是一个有效的日期字符串
    """
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def form_time_to_year_mon_day(_time):
    """
    解析数字形式的日期 为 year-mon-day
    """
    time_str = str(_time)
    year_mon_day = None
    if len(time_str) == 6:
        year_s = time_str[:4]
        mon_s = time_str[4:6]
        # print((int(year_s), int(mon_s), int(day_s)))
        year_mon_day = '%s-%s-01' % (year_s, mon_s)
    elif len(time_str) == 8:
        year_s = time_str[:4]
        mon_s = time_str[4:6]
        day_s = time_str[6:8]
        # print((int(year_s), int(mon_s), int(day_s)))
        year_mon_day = '%s-%s-%s' % (year_s, mon_s, day_s)

    if is_vaild_date(year_mon_day):
        return year_mon_day
    else:
        raise ValueError(time_str + '不是有效的日期')


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


def millisecond_to_timecode(millisecond):
    """
    毫秒转换为时间码字符串 01:02:03,000
    """
    return '%02d:%02d:%02d,%03d' % (
        millisecond / 3600000, (millisecond % 3600000) / 60000, (millisecond % 60000) / 1000, millisecond % 1000)


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


def time_str_to_second(time_str):
    """
    把人类阅读的时间转换为秒，用来和 second_to_time_str 函数互相转换
    例如：time_str_to_second('1小时1分1.099秒') 返回 3661.099
    """

    if '秒' not in time_str:
        return None

    seconds = 0.0

    if '小时' in time_str:
        hour, time_str = time_str.split('小时')
        seconds += int(hour.strip()) * 3600

    if '分' in time_str:
        minute, time_str = time_str.split('分')
        seconds += int(minute.strip()) * 60

    seconds += float(time_str.strip().replace('秒', ''))

    return seconds


class Timer:
    """
    计时器，可以当装饰器或者用 with 来对代码计时

    # 例子：
        >>> import time
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> with Timer() as timer:
        >>>     papapa(1)
        运行时间 1.000 秒
        >>> @Timer.time_it
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> papapa(1)
        papapa 运行时间 1.001 秒
    """

    def __init__(self, name=None):
        self.start = time.time()

        # 我们添加一个自定义的计时名称
        if isinstance(name, str):
            self.name = name + ' '
        else:
            self.name = ''

        print(f'{get_now()} 开始运行 {self.name}', )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running_time()
        return exc_type is None

    @staticmethod
    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f'{get_now()} 开始运行 {func.__name__}', )
            result = func(*args, **kwargs)
            print(f'{get_now()} 结束运行 {func.__name__}，运行时间 {second_to_time_str(time.time() - start)}', )
            return result

        return wrapper

    def running_time(self):
        stop = time.time()
        cost = stop - self.start
        print(f'{get_now()} 结束运行 {self.name}，运行时间 {second_to_time_str(cost)}', )


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=timestamp_to_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=timestamp13_to_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_to_timestamp)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=now_to_timestamp)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=timestamp_to_timestamp10)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=now_to_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_now)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_now_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_now_time)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_style_transfomation)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=is_vaild_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=form_time_to_year_mon_day)
    # youtube_dl\utils.py
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=date_from_str)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=hyphenate_date)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=DateRange)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=srt_subtitles_timecode)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=millisecond_to_timecode)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=second_to_time_str)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------

    start_time = t1 = time.time()

    doc()

    # # 例子
    # print(now_to_date())
    # print(timestamp_to_date(1516641825))
    # print(timestamp13_to_date(1516641825000))
    # print(date_to_timestamp('2018-01-23 01:23:45'))
    # print(timestamp_to_timestamp10(1516641825000))
    # print(date_style_transfomation('2018-01-23 01:23:45'))
    # # 结果为：
    # # 2018-11-15 11:19:23
    # # 2018-01-23 01:23:45
    # # 2018-01-23 01:23:45
    # # 1516641825
    # # 1516641825
    # # 2018-01-23 01-23-45

    print('运行时间 %.2f 秒' % (time.time() - start_time))

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


"""

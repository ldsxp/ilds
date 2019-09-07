# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：spider.py
#   版本：0.3
#   作者：lds
#   日期：2018-11-26
#   语言：Python 3.X
#   说明：爬虫用到的函数集合
# ---------------------------------------


import os
# import datetime
from time import time, sleep
# random_sleep
import random
# get_response
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException
# download_file
import re
from ilds.file import is_file
from urllib import parse


def random_sleep(start=1, end=3):
    """
    随机延迟，因为如果你访问了很多页面，你的ip可能会被封。
    :param start:
    :param end:
    :return:
    """
    sleep_time = random.randint(start, end)
    # sleep_time = random.randint(250, 1000) / 1000.0
    print('随机延迟：%s 秒......' % sleep_time)
    sleep(sleep_time)


def get_response(url, params=None, **kwargs):
    """
    请求获取网页内容，为了防止程序中断，捕捉错误，返回 None。
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    try:
        response = requests.get(url, params=params, **kwargs)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None, ):
    """
    长链接会话，支持重试

    例子：
    from requests.exceptions import ConnectTimeout, ConnectionError, ProxyError

    TIMEOUT = 5
    DEFAULT_RETRIES = 3
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }
    proxies = None
    session = requests_retry_session()
    url = 'https://www.baidu.com'
    for i in range(DEFAULT_RETRIES):
        try:
            r = session.get(url,
                            proxies=proxies, timeout=TIMEOUT,
                            headers=HEADERS)
        except ProxyError:
            print(f'Proxy {proxies} is dead!')
        except (ConnectTimeout, ConnectionError):
            pass
        else:
            break
    print(r.text)
    :param retries:
    :param backoff_factor:
    :param status_forcelist:
    :param session:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,  # 允许的重试总次数，优先于其他计数
        read=retries,  # 重试读取错误的次数
        connect=retries,
        backoff_factor=backoff_factor,  # 休眠时间： {backoff_factor} * (2 ** ({重试总次数} - 1))
        status_forcelist=status_forcelist,  # 强制重试的状态码
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_response_to_file(url, file_name=None, params=None, **kwargs):
    """
    请求获取网页内容，并保存到文件。
    :param url:
    :param file_name:
    :param params:
    :param kwargs:
    :return:
    """

    if file_name is None:
        file_name = url.split('/')[-1]
        file_name = re.sub('[\/:*?"<>|]', '-', file_name)

    ret = get_response(url, params=params, **kwargs)
    if ret:
        with open(file_name, 'w', encoding='utf-8') as fout:  # , encoding = 'utf-8'
            fout.write(ret.text)
        return file_name
    else:
        return None


def get_file_content(file_name=None):
    """
    读取文件内容
    :param file_name:
    :return:
    """
    # 写入本地文件
    # file = '测试.html'
    # with open(file, 'w', encoding='utf-8') as fout:  # , encoding = 'utf-8'
    #     fout.write(r.text)
    if not is_file(file_name):
        return None
    with open(file_name, 'r', encoding='utf-8') as fin:
        # content = fin.read()
        return fin.read()


def download_file(url, file_name=None):
    """
    下载文件
    :param url:
    :param file_name:
    :return:
    """

    r = requests.get(url, stream=True)
    # print(type(r.headers.get('Content-Disposition')))
    content_disposition = r.headers.get('Content-Disposition')

    if file_name is None:
        if content_disposition and 'attachment; filename="' in content_disposition:
            file_name = content_disposition[22:-1]
        else:
            file_name = url.split('/')[-1]
            file_name = re.sub('[\/:*?"<>|]', '-', file_name)

    file_size = r.headers.get('Content-Length')
    if file_size is None:
        # pprint(r.headers)
        print('文件大小获取失败，%s 不是合法文件......' % file_name)
        return None

    print("开始下载：%s \n文件大小：%s" % (file_name, file_size))

    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    print("%s 下载完成!\n" % file_name)
    return file_name


def url_to_dict(url):
    """把url转换为dict字典"""
    params = {}
    url = parse.unquote(url)
    for param in url.split('&'):
        # print(param)
        k, v = param.split('=')
        params[k] = v
        # print("'{}': '{}',".format(k, v),)
    return params


def get_cookie_dict(cookie):
    """转换 Raw 格式的 Cookie 为字典格式"""
    params = {}
    cookie = cookie.strip()
    if cookie.startswith('Cookie:'):
        cookie = cookie[7:].strip()
    for param in cookie.split(';'):
        k, v = param.split('=')
        params[k.strip()] = v.strip()
        # print("'{}': '{}',".format(k, v), )
    return params


def doc():
    """
    打印模块说明文档
    """
    doc_text = """
路径和网址url互相转换
    from urllib.request import pathname2url
    from urllib.request import url2pathname
    str2 = parse.quote(str1)  # url 编码
    str3 = parse.unquote(str2)  # url 解码
    """
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=random_sleep)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_response)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_response_to_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_file_content)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=download_file)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=url_to_dict)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_cookie_dict)

    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

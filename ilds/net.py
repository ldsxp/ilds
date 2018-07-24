# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：net.py
#   版本：0.1
#   作者：lds
#   日期：2018-07-05
#   语言：Python 3.X
#   说明：网络相关的函数集合
# ---------------------------------------

import socket


def get_host_ip():
    """
    通过 UDP 获取本机 IP
    print(get_host_ip())
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_host_ip)
    # doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=dict_val_to_key)
    # doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=list_to_dict)
    # doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_kuohao_feijie)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

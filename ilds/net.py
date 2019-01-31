# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：net.py
#   版本：0.2
#   作者：lds
#   日期：2019-01-31
#   语言：Python 3.X
#   说明：网络相关的函数集合
# ---------------------------------------

import os
import uuid
import socket
import struct

BROADCAST_IP = '255.255.255.255'
DEFAULT_PORT = 9


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


def get_mac_address():
    """
    获取本机 MAC 地址
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])  # .upper()


def get_arp_list():
    """
    获取局域网 ARP 表

    返回：[[id地址, mac], ]
    """
    host = get_host_ip()
    os.system('arp -a > arp_a.txt')
    arp_list = []
    with open('temp.txt') as fp:
        for line in fp:
            line = line.split()[:2]
            if line and line[0].startswith(host[:4]) and (not line[0].endswith('255')):
                arp_list.append(line)
                # print(':'.join(line))
    return arp_list


# https://github.com/remcohaszing/pywakeonlan
def create_magic_packet(macaddress):
    """
    创建一个魔术包。

    Magic Packet（魔法数据包）是一种数据包，可以与用于唤醒 LAN 协议一起使用来唤醒计算机。 数据包由作为参数给出的 mac 地址构成。

    需要主板的支持，操作系统要求：
    1. 网络属性 》 配置 》 Microsoft 网络客户端 》 属性 》 高级 》 启用 唤醒魔包
    2. 网络属性 》 配置 》 Microsoft 网络客户端 》 属性 》 电源管理 》 取消 允许计算机关闭此设备电源以节约电源

    备注：
    Magic Packet(魔法数据包)。一般通过 UDP 协议进行广播。端口一般是 7 或者 9。
    魔法数据包总是以"FF FF FF FF FF FF" 连续 6 个 "FF"，后面是 MAC 地址信息，一旦网卡侦测到数据包内容，就会唤醒目标计算机。

    # 本地关机命令
    import os
    os.system('shutdown -s -t 00')

    Args:
        macaddress (str): 解析为魔术包的 mac 地址。

    """
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('MAC 地址格式不正确')

    # 填充同步流
    data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
    send_data = b''

    # 拆分包中的十六进制值
    for i in range(0, len(data), 2):
        send_data += struct.pack(b'B', int(data[i: i + 2], 16))
    return send_data


def send_magic_packet(*macs, **kwargs):
    """
    唤醒局域网中的计算机。

    必须在主机设备上启用 LAN 唤醒。

    Args:
        macs (str): 唤醒机器的一个或多个 mac 地址。

    Keyword Args:
        ip_address (str): 发送魔术包的主机的IP地址 (default "255.255.255.255")
        port (int): 发送魔术包的主机端口 (default 9)


    例子：
    from ilds.net import send_magic_packet

    # 通过其 mac 地址唤醒单台计算机
    send_magic_packet('ff.ff.ff.ff.ff.ff')

    # 通过他们的mac地址唤醒多台计算机。
    send_magic_packet('ff.ff.ff.ff.ff.ff', '00-00-00-00-00-00', 'FFFFFFFFFFFF')

    # 可以指定外部主机。请注意，该主机上的端口转发是必需的。默认IP地址为 255.255.255.255，默认端口为9。
    send_magic_packet('ff.ff.ff.ff.ff.ff', ip_address='example.com', port=1337)
    """
    packets = []
    ip = kwargs.pop('ip_address', BROADCAST_IP)
    port = kwargs.pop('port', DEFAULT_PORT)
    for k in kwargs:
        raise TypeError('send_magic_packet() got an unexpected keyword '
                        'argument {!r}'.format(k))

    for mac in macs:
        packet = create_magic_packet(mac)
        packets.append(packet)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    for packet in packets:
        sock.send(packet)
    sock.close()


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_host_ip)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_mac_address)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=get_arp_list)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=send_magic_packet)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

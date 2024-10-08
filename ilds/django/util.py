# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：util.py
#   版本：0.4
#   作者：lds
#   日期：2024-09-18
#   语言：Python 3.X
#   说明：常用的函数集合
# ---------------------------------------
import os
import sys
import random

from ilds.util import CLEAN_STR


# https://stackoverflow.com/questions/8047204/django-script-to-access-model-objects-without-using-manage-py-shell
def django_setup(project_name=None, site_path=None):
    """
    设置 Django 运行环境

    用法示例:
    from ilds.django.util import django_setup
    django_setup(r'mysite', site_path=None)
    """

    if site_path:
        sys.path.insert(0, site_path)

    if not project_name:
        project_name = os.path.basename(os.path.dirname(__file__))

    print(f'项目：{project_name}')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")

    try:
        import django
        django.setup()
    except ModuleNotFoundError as e:
        print("注：如果找不到 Django，请安装它: pip install django\n错误提示：", e)
        exit(1)  # 使用非零退出代码表示程序异常退出
    except Exception as e:
        print("发生了意外错误：", e)
        exit(1)


def random_key():
    """
    生成 Django 使用的 SECRET_KEY

    from ilds.django.util import random_key
    print(random_key())
    """

    return ''.join(
        [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += 'CLEAN_STR\n    需要清洗的字符（用在歌曲名，表演者匹配的时候）\n\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=django_setup)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=random_key)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

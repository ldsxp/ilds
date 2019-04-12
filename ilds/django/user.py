# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：user.py
#   版本：0.1
#   作者：lds
#   日期：2019-01-21
#   语言：Python 3.X
#   说明：django 用户相关的函数集合
# ---------------------------------------

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password  # , check_password

User = get_user_model()


def add_superuser(username, email, password):
    """
    添加 django 超级用户

    from ilds.django.user import add_superuser
    add_superuser(username='admin', email='admin@qq.com', password='123456')
    """
    if not password.startswith('pbkdf2_'):
        password = make_password(password)

    # 添加一个超级用户数据
    add_user = User.objects.create(**{
        'password': password,
        'last_login': None,
        'is_superuser': True,
        'username': username,
        'email': email,
        'is_staff': True,
        'is_active': True})

    try:
        from allauth.account.models import EmailAddress  # django-allauth
        EmailAddress.objects.create(**{
            'user': add_user,
            'email': email,
            'verified': True,
            'primary': True})
    except Exception as e:
        print(e)

    return True


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=add_superuser)
    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))

import os
import sys
from setuptools import setup, find_packages

from ilds.versions import version

# find_packages()
# 对于简单工程来说，手动增加packages参数很容易，这个函数默认在和setup.py同一目录下搜索各个含有 __init__.py的包。
# 其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有 aaa.txt 文件和 data 数据文件夹。
# 另外，也可以排除一些特定的包：
# find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

# 检查 setup.py 是不是正确，如果只输出 running check，那么就ok了
# python setup.py check

# 打包
# python setup.py sdist
# 把安装包加入到官方的pip服务器
# 首先注册一个pip账号（https://pypi.python.org/pypi）
# 注册自己的包名以及上传需要运行命令 python setup.py register sdist upload 按照要求填写自己的用户名密码即可。
# 此时只需要 pip install mypackage 就能够安装自己的包，超级方便。
# 自己的包修改之后，修改 setup.py 中的版本号即可再次更新上传。
# 有时更新较频繁会导致 pip 从缓存中获取数据而不是服务器上的最新版本，运行 pip 时加上 --no-cache-dir 选项即可解决。


# setup.py文件的使用：
# python setup.py build # 编译
# python setup.py install    # 安装
# python setup.py sdist     # 制作分发包
# python setup.py sdist build  # 打包为tar.gz
# python setup.py sdist bdist_wheel # 打包 wheels 格式的包
# python setup.py bdist_wininst # 制作windows下的分发包
# python setup.py bdist_rpm

# https://pypi.org/project/ilds/
"""

pip install -U ilds
pip --no-cache-dir install -U ilds

# 打包需要安装 twine
# 如果报错：error: invalid command 'bdist_wheel'，多半是 setuptools 版本不正确或者没有安装 wheel

# 处理pip升级失败
# python -m pip install --upgrade pip 更新失败 卸载 python -m pip uninstall pip 安装 easy_install.exe pip 不能解决！
# 用这个命令升级：easy_install -U pip

# 检查错误
# twine check dist/*

echo 使用 twine 上传到官方的pip服务器:
echo 在系统添加 TWINE_USERNAME 和 TWINE_PASSWORD 变量，不用输入用户名和密码
rmdir /S/Q build
rmdir /S/Q dist
python setup.py sdist bdist_wheel
echo 上传到PyPI:
twine upload dist/*


# 本地安装（不推荐在生产环境使用）
PyCharm > Terminal
cd tools\lds&python setup.py sdist
pip install -U dist\lds-0.0.8.tar.gz



pip install -U "/Users/lds/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/tools/lds/dist/lds-0.0.8.tar.gz"

"""

# twine upload dist/* 使用 twine 上传
# 添加上传到 PyPI 的命令
# 设置 TWINE_USERNAME=lds 和 TWINE_PASSWORD 变量，但不建议设置到系统里面
# 勾选：Emulate terminal in output console(在输出控制台中模拟终端)
if sys.argv[-1] == 'up':
    # os.system('rm -rf dist')
    # os.system('rm -rf build')
    os.system('rmdir /S/Q build')
    os.system('rmdir /S/Q dist')
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


# error: invalid command 'bdist_wheel' 需要安装wheel ： pip install -U wheel
# 读取 README.md 文件内容
def read_md_convert(f):
    return convert(f, 'md')


def read_md_open(f):
    return open(f, 'r').read()


try:
    from pypandoc import convert

    read_md = read_md_convert
except ImportError:
    read_md = read_md_open

setup(
    # 名称
    name="ilds",
    # 版本
    version=version,
    # version=".".join(map(str, __import__('html2text').__version__)),
    # 关键字列表
    # keywords = ("test", "xxx"),
    # 简单描述
    description="常用模块的集合，为了多平台，多电脑调用方便!",
    # 详细描述
    # long_description = "常用爬虫功能的封装",
    # long_description = read_md('README.md'),
    long_description=open('README.rst', encoding='utf-8').read(),
    # 授权信息
    license="GNU GPL 3",

    # 官网地址
    url="https://github.com/ldsxp/ilds",
    # 程序的下载地址
    download_url="https://pypi.org/project/ilds",
    # 作者
    author="lds",
    # 作者的邮箱地址
    author_email="85176878@qq.com",
    # 维护者
    # maintainer = "lds2",
    # 维护者的邮箱地址
    # maintainer_email = "85176878@qq.com",

    # 需要处理的包目录（包含__init__.py的文件夹）
    packages=find_packages(),
    # packages = ['lds'],
    # 需要打包的python文件列表
    # py_modules = "any",
    # 需要打包的数据文件，如图片，配置文件等
    # data_files = "a.jpg"
    # 使用 MANIFEST.in 设置 include_package_data
    # include_package_data = True,
    # 软件平台列表
    platforms="any",
    # 所属分类列表
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3.4',  # 我们为了在老版系统安装，添加了这个，但是大部分功能都不支持 3.4
        'Programming Language :: Python :: 3.6',
    ],
    # 需要安装的依赖包
    install_requires=[
        'xlrd>=1.1.0',
        'colorama',
        'chardet',
        'pyperclip',
        'requests',
        'html2text',
        'mistune',
        'openpyxl',
        # 'setuptools>=16.0',
        # '+++',
    ],

    # 此项需要，否则卸载时报windows error
    # zip_safe = False

    #  安装时需要执行的脚步列表
    # scripts = [],
    # 告诉setuptools哪些目录下的文件被映射到哪个源码包。
    # package_dir = {'': 'lib'} # 表示“root package”中的模块都在lib 目录中
    # 定义依赖哪些模块
    # requires
    # 定义可以为哪些模块提供依赖
    # provides
    #  动态发现服务和插件
    # entry_points = {
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
    # entry_points="""
    #     [console_scripts]
    #     html2text=html2text.cli:main
    # """,
)

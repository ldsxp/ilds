# import os
# import sys
# from setup import version
#
# print(sys.argv)

# 把包发布在PyPI上时，我只需要打下：
# python lds.py install
# if sys.argv[-1] == 'publish':
#     os.system("python setup.py sdist upload")
#     os.system("python setup.py bdist_wheel upload")
#     sys.exit()
#
# if sys.argv[-1] == 'lds':
#     print(os.system("python -V"))
#     os.system("python setup.py sdist")
#     os.chdir(os.path.join(os.getcwd(), 'dist'))
#     os.system("pip install -U lds-%s.tar.gz" % version)
#     sys.exit()
#
# if sys.argv[-1] == 'tag':
#     os.system("git tag -a %s -m 'version %s'" % (version, version))
#     os.system("git push --tags")
#     sys.exit()


import requests

# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to':'rst','from':'markdown'},
                      files={'input_files[]':open(from_file,'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.rst", "README2.rst")
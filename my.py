import os
import sys
from setup import version

print(sys.argv)

# 把包发布在PyPI上时，我只需要打下：
# python lds.py install
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == 'lds':
    print(os.system("python -V"))
    os.system("python setup.py sdist")
    os.chdir(os.path.join(os.getcwd(), 'dist'))
    os.system("pip install -U lds-%s.tar.gz" % version)
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

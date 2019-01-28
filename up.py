import os
# import sys


os.system('rm -rf dist')
os.system('rm -rf build')
os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')
# sys.exit()
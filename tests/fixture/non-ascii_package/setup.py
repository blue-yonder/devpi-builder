# encoding=utf-8

import multiprocessing  # avoid crash on teardown
from setuptools import setup, find_packages

import sys

if 'bdist_wheel' in sys.argv:
    print('Nööp! Нет! No non-ascii 4 you!')
    sys.exit(1)

setup(
    name='non-ascii-package',
    version='0.1.dev1',
    packages=find_packages(exclude=['tests']),
)

import multiprocessing # avoid crash on teardown
from setuptools import setup, find_packages

setup(
    name = 'test-package',
    version = '0.1-dev',
    packages = find_packages(exclude=['tests']),
)

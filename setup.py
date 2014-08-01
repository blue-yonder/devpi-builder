# coding=utf-8

__author__ = 'mbach'

import multiprocessing # avoid crash on teardown
from setuptools import setup, find_packages


setup(
    name = 'devpi-builder',
    version = '0.1.0',
    packages = find_packages(exclude=['tests']),
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    description='Fill in index with wheels from an requirements.txt-like specification file.',
    license='new BSD',
    install_requires=[
        'setuptools',
        'devpi-client',
        'wheel'
    ],
    setup_requires=[
        'nose>=1.0'
    ],
    tests_require=[
        'nose>=1.0',
        'devpi-server'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Archiving :: Packaging'
    ],
      entry_points={
        'console_scripts': [
            'devpi-builder = devpi_builder.cli:main',
        ],
      },
)

__author__ = 'mbach'

import multiprocessing # avoid crash on teardown
from setuptools import setup, find_packages


setup(
    name = 'Brandon',
    version = '0.1-dev',
    packages = find_packages(exclude=['tests']),
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    description='Fill in index with wheels from an requirements.txt-like specification file.',
    license='Proprietary',
    install_requires=[
        'setuptools'
    ],
    setup_requires=[
        'nose>=1.0'
    ],
    tests_require=[
        'nose>=1.0'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Topic :: System :: Archiving :: Packaging'
    ]
)
# coding=utf-8

import multiprocessing  # avoid crash on teardown
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='devpi-builder',
    version='0.3.0',
    packages=find_packages(exclude=['tests']),
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    description='Devpi-builder takes a requirements.txt and incrementally fills a devpi index with wheels of the listed python packages.',
    long_description=readme,
    license='new BSD',
    install_requires=[
        'setuptools',
        'devpi-client',
        'wheel',
        'pip>=1.5.3',
        'junit-xml'
    ],
    setup_requires=[
        'nose>=1.0'
    ],
    tests_require=[
        'nose>=1.0',
        'mock',
        'coverage',
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

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()
with open('CHANGELOG.rst') as f:
    changelog = f.read()

setup(
    name='devpi-builder',
    use_scm_version=True,
    packages=find_packages(exclude=['tests']),
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    url='https://github.com/blue-yonder/devpi-builder',
    description='Devpi-builder takes a requirements.txt and incrementally fills a devpi index with wheels of the listed python packages.',
    long_description='%s\n\n%s' % (readme, changelog),
    license='new BSD',
    install_requires=[
        'devpi-plumber>=0.2.14',
        'setuptools',
        'wheel',
        'wheel-filename',
        'wheel-inspect>=1.6.0',
        'pip>=1.5.3',
        'junit-xml'
    ],
    python_requires='>=3.6',
    setup_requires=[
        'setuptools_scm',
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'mock',
        'devpi-plumber[test]>=0.4.3',
    ],
    test_suite='pytest-runner',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Archiving :: Packaging',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'devpi-builder = devpi_builder.cli:main',
        ],
    },
)

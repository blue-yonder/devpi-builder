# coding=utf-8

import os.path as path
import re

import pytest

from devpi_builder import wheeler


class BuilderTest(object):
    def test_build(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
            assert re.match(r'.*\.whl$', wheel_file)
            assert path.exists(wheel_file)

    def test_cleans_up_created_files(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
        assert not path.exists(wheel_file)

    def test_provides_file_that_is_already_a_wheel(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('wheel', '0.24')
            assert path.exists(wheel_file)

    def test_throws_custom_on_build_failure(self):
        with wheeler.Builder() as builder:
            with pytest.raises(wheeler.BuildError) as info:
                builder('package_that_hopefully_does_not_exist', '99.999')
            info.match(r'(Could not find a version that satisfies the requirement package[-_]that[-_]hopefully[-_]does[-_]not[-_]exist==99.999 \(from versions: \))|(Could not find any downloads that satisfy the requirement package-that-hopefully-does-not-exist==99.999)')

    def test_look_for_non_existing_wheel(self):
        builder = wheeler.Builder()
        with builder:
            with pytest.raises(wheeler.BuildError):
                builder._find_wheel('nothing_can_be_found', '1.1')


def test_is_pure():
    assert wheeler.is_pure('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')
    assert not wheeler.is_pure('tests/fixture/non-pure_package/dist/test_package-0.1.dev1-cp27-none-linux_x86_64.whl')


def test_is_compatible():
    assert wheeler.is_compatible('http://localhost:1234/good-1.0-py2.py3-none-any.whl')


def test_is_incompatible():
    assert not wheeler.is_compatible('http://localhost:1234/bad-1.0-py99-none-any.whl')
    assert not wheeler.is_compatible('http://localhost:1234/bad-1.0.tar.gz')


def test_has_compatible():
    packages = ['http://localhost:1234/good-1.0-py2.py3-none-any.whl', 'http://localhost:1234/bad-1.0-py99-none-any.whl']
    assert wheeler.has_compatible_wheel(packages)


def test_has_no_compatible():
    packages = ['http://localhost:1234/sdist-1.0.tar.gz', 'http://localhost:1234/bad-1.0-py99-none-any.whl']
    assert not wheeler.has_compatible_wheel(packages)

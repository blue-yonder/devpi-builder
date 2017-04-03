# coding=utf-8

import pytest

from devpi_builder import requirements


def test_read_requirements():
    expected = [
        ('progressbar', '2.2'),
        ('six', '1.7.3')
    ]
    assert expected == requirements.read('tests/fixture/sample_simple.txt')


def test_multiple_versions():
    expected = [
        ('progressbar', '2.2'),
        ('progressbar', '2.1')
    ]
    assert expected == requirements.read('tests/fixture/sample_multiple_versions.txt')


def test_fail_on_inexact():
    with pytest.raises(ValueError):
        requirements.read('tests/fixture/sample_inexact_version.txt')


def test_fail_on_no_version():
    with pytest.raises(ValueError):
        requirements.read('tests/fixture/sample_no_version.txt')


def test_fail_on_multiple_versions_on_line():
    with pytest.raises(ValueError):
        requirements.read('tests/fixture/sample_multiple_versions_on_line.txt')


def test_matched_by_file():
    filename = 'tests/fixture/sample_blacklist.txt'
    assert requirements.matched_by_file('any_version', 1.1, filename)
    assert not requirements.matched_by_file('not_mentioned', 0.3, filename)

    assert requirements.matched_by_file('version_1_0', 1.0, filename)
    assert not requirements.matched_by_file('version_1_0', 0.9, filename)

    assert requirements.matched_by_file('at_least_0_5', 1.0, filename)
    assert requirements.matched_by_file('at_least_0_5', 0.5, filename)
    assert not requirements.matched_by_file('at_least_0_5', 0.4, filename)

    assert requirements.matched_by_file('below_2_0', 1.0, filename)
    assert not requirements.matched_by_file('below_2_0', 2.0, filename)


def test_comments():
    expected = [
        ('progressbar', '2.2')
    ]
    assert expected == requirements.read('tests/fixture/sample_comments.txt')

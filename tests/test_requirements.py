# coding=utf-8

import pytest

from devpi_builder import requirements


def test_read_requirements():
    expected = [
        ('progressbar', '2.2'),
        ('six', '1.7.3')
    ]
    assert expected == requirements.read_exact_versions('tests/fixture/sample_simple.txt')


def test_multiple_versions():
    expected = [
        ('progressbar', '2.2'),
        ('progressbar', '2.1')
    ]
    assert expected == requirements.read_exact_versions('tests/fixture/sample_multiple_versions.txt')


def test_fail_on_inexact():
    with pytest.raises(ValueError):
        requirements.read_exact_versions('tests/fixture/sample_inexact_version.txt')


def test_fail_on_no_version():
    with pytest.raises(ValueError):
        requirements.read_exact_versions('tests/fixture/sample_no_version.txt')


def test_fail_on_multiple_versions_on_line():
    with pytest.raises(ValueError):
        requirements.read_exact_versions('tests/fixture/sample_multiple_versions_on_line.txt')


def test_matched_by_list():
    parsed = requirements.read_raw('tests/fixture/sample_blacklist.txt')
    assert requirements.matched_by_list('any_version', 1.1, parsed)
    assert not requirements.matched_by_list('not_mentioned', 0.3, parsed)

    assert requirements.matched_by_list('version_1_0', 1.0, parsed)
    assert not requirements.matched_by_list('version_1_0', 0.9, parsed)

    assert requirements.matched_by_list('at_least_0_5', 1.0, parsed)
    assert requirements.matched_by_list('at_least_0_5', 0.5, parsed)
    assert not requirements.matched_by_list('at_least_0_5', 0.4, parsed)

    assert requirements.matched_by_list('below_2_0', 1.0, parsed)
    assert not requirements.matched_by_list('below_2_0', 2.0, parsed)


def test_comments():
    expected = [
        ('progressbar', '2.2')
    ]
    assert expected == requirements.read_exact_versions('tests/fixture/sample_comments.txt')


def test_read_raw_without_file():
    assert [] == requirements.read_raw(None)

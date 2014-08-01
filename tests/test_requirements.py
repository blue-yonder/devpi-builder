# coding=utf-8

__author__ = 'mbach'

import unittest

from devpi_builder import requirements


class TestRequirements(unittest.TestCase):
    def test_read_requirements(self):
        expected = [
            ('progressbar', '2.2'),
            ('six', '1.7.3')
        ]
        self.assertListEqual(
            expected,
            requirements.read('tests/sample_simple.txt')
        )

    def test_multiple_versions(self):
        expected = [
            ('progressbar', '2.2'),
            ('progressbar', '2.1')
        ]
        self.assertListEqual(
            expected,
            requirements.read('tests/sample_multiple_versions.txt')
        )

    def test_fail_on_inexact(self):
        with self.assertRaises(ValueError):
            requirements.read('tests/sample_inexact_version.txt')

    def test_fail_on_multiple_versions_on_line(self):
        with self.assertRaises(ValueError):
            requirements.read('tests/sample_multiple_versions_on_line.txt')


if __name__ == '__main__':
    unittest.main()

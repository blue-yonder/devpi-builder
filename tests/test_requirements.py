# coding=utf-8

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
            requirements.read('tests/fixture/sample_simple.txt')
        )

    def test_multiple_versions(self):
        expected = [
            ('progressbar', '2.2'),
            ('progressbar', '2.1')
        ]
        self.assertListEqual(
            expected,
            requirements.read('tests/fixture/sample_multiple_versions.txt')
        )

    def test_fail_on_inexact(self):
        with self.assertRaises(ValueError):
            requirements.read('tests/fixture/sample_inexact_version.txt')

    def test_fail_on_no_version(self):
        with self.assertRaises(ValueError):
            requirements.read('tests/fixture/sample_no_version.txt')

    def test_fail_on_multiple_versions_on_line(self):
        with self.assertRaises(ValueError):
            requirements.read('tests/fixture/sample_multiple_versions_on_line.txt')

    def test_matched_by_file(self):
        filename = 'tests/fixture/sample_blacklist.txt'
        self.assertTrue(requirements.matched_by_file('any_version', 1.1, filename))
        self.assertFalse(requirements.matched_by_file('not_mentioned', 0.3, filename))

        self.assertTrue(requirements.matched_by_file('version_1_0', 1.0, filename))
        self.assertFalse(requirements.matched_by_file('version_1_0', 0.9, filename))

        self.assertTrue(requirements.matched_by_file('at_least_0_5', 1.0, filename))
        self.assertTrue(requirements.matched_by_file('at_least_0_5', 0.5, filename))
        self.assertFalse(requirements.matched_by_file('at_least_0_5', 0.4, filename))

        self.assertTrue(requirements.matched_by_file('below_2_0', 1.0, filename))
        self.assertFalse(requirements.matched_by_file('below_2_0', 2.0, filename))

    def test_comments(self):
        expected = [
            ('progressbar', '2.2')
        ]
        self.assertListEqual(
            expected,
            requirements.read('tests/fixture/sample_comments.txt')
        )

if __name__ == '__main__':
    unittest.main()

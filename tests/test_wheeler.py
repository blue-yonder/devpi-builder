# coding=utf-8

import os.path as path
import unittest

from devpi_builder import wheeler


class WheelTest(unittest.TestCase):
    def test_build(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
            self.assertRegexpMatches(wheel_file, '\.whl$')
            self.assert_(path.exists(wheel_file))

    def test_cleans_up_created_files(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
        self.assertFalse(path.exists(wheel_file))

    def test_provides_file_that_is_already_a_wheel(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('wheel', '0.24')
            self.assert_(path.exists(wheel_file))

    def test_throws_custom_on_build_failure(self):
        with wheeler.Builder() as builder:
            with self.assertRaises(wheeler.BuildError):
                builder('package_that_hopefully_does_not_exist', '99.999')

    def test_look_for_non_existing_wheel(self):
        builder = wheeler.Builder()
        with builder:
            with self.assertRaises(wheeler.BuildError):
                builder._find_wheel('nothing_can_be_found', '1.1')

if __name__ == '__main__':
    unittest.main()

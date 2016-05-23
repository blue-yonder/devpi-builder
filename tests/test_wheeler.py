# coding=utf-8

import os.path as path
import unittest

from devpi_builder import wheeler


class BuilderTest(unittest.TestCase):
    def test_build(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
            self.assertRegexpMatches(wheel_file, '\.whl$')
            self.assertTrue(path.exists(wheel_file))

    def test_cleans_up_created_files(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
        self.assertFalse(path.exists(wheel_file))

    def test_provides_file_that_is_already_a_wheel(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('wheel', '0.24')
            self.assertTrue(path.exists(wheel_file))

    def test_throws_custom_on_build_failure(self):
        with wheeler.Builder() as builder:
            with self.assertRaisesRegexp(wheeler.BuildError, r'Could not find a version that satisfies the requirement package-that-hopefully-does-not-exist==99.999 \(from versions: \)'):
                builder('package_that_hopefully_does_not_exist', '99.999')

    def test_look_for_non_existing_wheel(self):
        builder = wheeler.Builder()
        with builder:
            with self.assertRaises(wheeler.BuildError):
                builder._find_wheel('nothing_can_be_found', '1.1')


class WheelerTest(unittest.TestCase):
    def test_is_pure(self):
        self.assertTrue(wheeler.is_pure('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl'))
        self.assertFalse(wheeler.is_pure('tests/fixture/non-pure_package/dist/test_package-0.1.dev1-cp27-none-linux_x86_64.whl'))

    def test_is_compatible(self):
        self.assertTrue(wheeler.is_compatible('http://localhost:1234/good-1.0-py2.py3-none-any.whl'))

    def test_is_incompatible(self):
        self.assertFalse(wheeler.is_compatible('http://localhost:1234/bad-1.0-py99-none-any.whl'))
        self.assertFalse(wheeler.is_compatible('http://localhost:1234/bad-1.0.tar.gz'))

    def test_has_compatible(self):
        packages = ['http://localhost:1234/good-1.0-py2.py3-none-any.whl', 'http://localhost:1234/bad-1.0-py99-none-any.whl']
        self.assertTrue(wheeler.has_compatible_wheel(packages))

    def test_has_no_compatible(self):
        packages = ['http://localhost:1234/sdist-1.0.tar.gz', 'http://localhost:1234/bad-1.0-py99-none-any.whl']
        self.assertFalse(wheeler.has_compatible_wheel(packages))


if __name__ == '__main__':
    unittest.main()

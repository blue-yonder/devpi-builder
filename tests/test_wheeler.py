import os.path as path
import unittest

from brandon import wheeler


__author__ = 'mbach'


class WheelTest(unittest.TestCase):
    def test_build(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
            self.assertRegexpMatches(wheel_file, '\.whl$')
            self.assert_(path.exists(wheel_file))

    @unittest.skip('not implemented')
    def test_cleans_up_created_files(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
        self.assertFalse(path.exists(wheel_file))

    @unittest.skip('not implemented')
    def test_provides_file_thats_already_a_wheel(self):
        with wheeler.Builder() as builder:
            wheel_file = builder('progressbar', '2.2')
            self.assert_(path.exists(wheel_file))

if __name__ == '__main__':
    unittest.main()

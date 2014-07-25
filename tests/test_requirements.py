__author__ = 'mbach'

import unittest

from brandon import requirements


class MyTestCase(unittest.TestCase):
    def test_read_requirements(self):
        expected = [
            ('progressbar', '2.0'),
            ('six', '1.3')
        ]
        self.assertListEqual(
            expected,
            requirements.read('tests/sample1.txt')
        )

    @unittest.skip('not implemented')
    def test_multiple_versions(self):
        pass

    @unittest.skip('not implemented')
    def test_fail_on_inexact(self):
        pass


if __name__ == '__main__':
    unittest.main()

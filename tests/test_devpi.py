# coding=utf-8

import sys
import unittest

from devpi_builder import devpi

from tests.tools import devpi_server, devpi_index


FAKE_SERVER = 'http://localhost:12345/'


class FakeClient(devpi.Client):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    _FAKE_RESULTS = {
        'list good_wheel==1.0': '%s/good-1.0-py2.py3-none-any.whl' % FAKE_SERVER,
        'list bad_wheel==1.0': '%s/bad-1.0-py99-none-any.whl' % FAKE_SERVER,
        'list invalid_package_name==14.234': '',
        }

    def _execute(self, *args):
        args_str = ' '.join(args)
        return self._FAKE_RESULTS[args_str]


class TestClient(unittest.TestCase):

    def test_check_for_package_version(self):
        with FakeClient('%s/test/wheels' % FAKE_SERVER) as devpi_client:
            self.assertTrue(devpi_client.package_version_exists('good_wheel', '1.0'))
            self.assertFalse(devpi_client.package_version_exists('bad_wheel', '1.0'))
            self.assertFalse(devpi_client.package_version_exists('invalid_package_name', '14.234'))

    def test_invalid_check_for_package_version(self):
        with devpi_server() as server_url:
            with devpi.Client(server_url + '/root/pypi') as devpi_client:
                with self.assertRaises(Exception):
                    self.assertTrue(devpi_client.package_version_exists('progressbar', ''))
                with self.assertRaises(Exception):
                    self.assertTrue(devpi_client.package_version_exists('progressbar', '?!'))

    def test_upload_package_version(self):
        # note that this test requires a bundled wheel for each supported
        # python version
        user = 'test'
        version_tuple = sys.version_info[:2]
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):
            with devpi.Client(server_url + '/test/wheels', user, password) as devpi_client:
                devpi_client.upload_dir('tests/fixture/non-pure_package/dist/')
                self.assertTrue(devpi_client.package_version_exists('test_package', '0.1-dev'))


if __name__ == '__main__':
    unittest.main()

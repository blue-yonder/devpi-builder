# coding=utf-8

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
        'list progressbar==2.2': ('%s/test/wheels/+f/924/023b6782e096a/numpy-1.9.0-cp27-none-linux_i686.whl'
                                  % FAKE_SERVER),
        'list invalid_package_name==14.234': '',
        }

    def _execute(self, *args):
        args_str = ' '.join(args)
        return self._FAKE_RESULTS[args_str]


class TestClient(unittest.TestCase):

    def test_check_for_package_version(self):
        with FakeClient('%s/test/wheels' % FAKE_SERVER) as devpi_client:
            # oslo.config 1.4.0.0a4 was only ever released as a wheel
            self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))
            self.assertFalse(devpi_client.package_version_exists('invalid_package_name', '14.234'))

    def test_invalid_check_for_package_version(self):
        with devpi_server() as server_url:
            with devpi.Client(server_url + '/root/pypi') as devpi_client:
                with self.assertRaises(Exception):
                    self.assertTrue(devpi_client.package_version_exists('progressbar', ''))
                with self.assertRaises(Exception):
                    self.assertTrue(devpi_client.package_version_exists('progressbar', '?!'))

    def test_upload_package_version(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):
            with devpi.Client(server_url + '/test/wheels', user, password) as devpi_client:
                devpi_client.upload('tests/fixture/non-pure_package/dist/test_package-0.1_dev-cp27-none-linux_x86_64.whl')
                self.assertTrue(devpi_client.package_version_exists('test_package', '0.1-dev'))


if __name__ == '__main__':
    unittest.main()

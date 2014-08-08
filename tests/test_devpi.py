# coding=utf-8

import unittest

from devpi_builder import devpi

from tests.tools import devpi_server, devpi_index


class TestClient(unittest.TestCase):

    def test_check_for_package_version(self):
        with devpi_server() as server_url:
            with devpi.Client(server_url + '/root/pypi') as devpi_client:
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

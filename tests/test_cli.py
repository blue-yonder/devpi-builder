# coding=utf-8

import unittest

from devpi_builder.cli import main
from devpi_builder import devpi

from tests.tools import devpi_server, devpi_index


class CliTest(unittest.TestCase):
    def test_basic(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/sample_simple.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))

    def test_with_blacklist(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/sample_simple.txt', destination_index, user, password, '--blacklist={}'.format('tests/sample_no_version.txt')])

            with devpi.Client(destination_index) as devpi_client:
                self.assertFalse(devpi_client.package_version_exists('progressbar', '2.2'))
                self.assertTrue(devpi_client.package_version_exists('six', '1.7.3'))

    def test_multiple_versions(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/sample_multiple_versions.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.1'))
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))


if __name__ == '__main__':
    unittest.main()

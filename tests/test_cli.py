# coding=utf-8

import unittest

from mock import patch

from devpi_builder.cli import main
from devpi_builder import devpi, wheeler

from tests.tools import devpi_server, devpi_index


class CliTest(unittest.TestCase):
    def test_basic(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_simple.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))

    def test_with_blacklist(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_simple.txt', destination_index, user, password, '--blacklist={}'.format('tests/fixture/sample_no_version.txt')])

            with devpi.Client(destination_index) as devpi_client:
                self.assertFalse(devpi_client.package_version_exists('progressbar', '2.2'))
                self.assertTrue(devpi_client.package_version_exists('six', '1.7.3'))

    def test_multiple_versions(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_multiple_versions.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.1'))
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))

    def test_reupload_is_safe(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_simple.txt', destination_index, user, password])
            main(['tests/fixture/sample_multiple_versions.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.1'))
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))
                self.assertTrue(devpi_client.package_version_exists('six', '1.7.3'))

    def test_continue_on_failed(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_continue_on_failed.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('progressbar', '2.2'))

    def test_different_styles(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):

            main(['tests/fixture/sample_different_styles.txt', destination_index, user, password])

            with devpi.Client(destination_index) as devpi_client:
                self.assertTrue(devpi_client.package_version_exists('pygments', '1.6'))
                self.assertTrue(devpi_client.package_version_exists('Pygments', '1.6'))
                self.assertTrue(devpi_client.package_version_exists('Django', '1.6.5'))
                self.assertTrue(devpi_client.package_version_exists('django', '1.6.5'))

    def test_not_built_if_on_pure(self):
        """
        Verify that packages are not built and re-uploaded if they are already on the pure index.
        """
        pure_user = 'pure'
        with devpi_server() as server_url:
            with devpi_index(server_url, 'destination', 'wheels') as (destination_index, _):
                with devpi_index(server_url, pure_user, 'pure') as (pure_index, pure_password):
                    with devpi.Client(pure_index, pure_user, pure_password) as client:
                        client.upload('tests/fixture/pure_package/dist/test_package-0.1_dev-py2.py3-none-any.whl')

                    with patch.object(wheeler.Builder, 'build', autospec=True, side_effect=Exception('Should not build!')) as mock_build:
                        main(['tests/fixture/sample_test_package.txt', destination_index, pure_user, pure_password,
                              '--pure-index={}'.format(pure_index)
                        ])

                        self.assertFalse(mock_build.called)

if __name__ == '__main__':
    unittest.main()

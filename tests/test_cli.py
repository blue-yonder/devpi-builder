# coding=utf-8
import os.path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

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

    def test_fills_proper_index(self):
        """
        Verify that pure packages are uploaded to the pure index non-pure packages are uploaded to the normal index.
        """
        user = 'user'
        with devpi_server() as server_url:
            with devpi_index(server_url, user, 'binary') as (binary_index, password):
                with devpi_index(server_url, user, 'pure', password) as (pure_index, _):
                    main(['tests/fixture/sample_pure_and_non-pure.txt', binary_index, user, password,
                          '--pure-index={}'.format(pure_index)
                    ])

                    with devpi.Client(pure_index) as client:
                        self.assertTrue(client.package_version_exists('progressbar', '2.2'))
                        self.assertFalse(client.package_version_exists('PyYAML', '3.10'))

                    with devpi.Client(binary_index) as client:
                        self.assertFalse(client.package_version_exists('progressbar', '2.2'))
                        self.assertTrue(client.package_version_exists('PyYAML', '3.10'))

    def _assert_test_case(self, root_element, result_tag_type, expected_element_name):
        xpath = './/testcase/{}/..'.format(result_tag_type)
        matched_nodes = root_element.findall(xpath)
        self.assertEqual(1, len(matched_nodes))
        self.assertEqual(matched_nodes[0].attrib['name'], expected_element_name)

    def test_reports_junit_xml(self):
        user = 'test'
        with devpi_server() as server_url, devpi_index(server_url, user, 'wheels') as (destination_index, password):
            with devpi.Client(destination_index, user, password) as client:
                client.upload('tests/fixture/pure_package/dist/test_package-0.1_dev-py2.py3-none-any.whl')

            tempdir = tempfile.mkdtemp()
            try:
                junit_filename = os.path.join(tempdir, 'junit.xml')
                main(['tests/fixture/sample_junit.txt', destination_index, user, password, '--junit-xml', junit_filename])

                root = ET.parse(junit_filename)
                self._assert_test_case(root, 'failure', 'package-that-hopefully-not-exists 99.999')
                self._assert_test_case(root, 'skipped', 'test-package 0.1-dev')
            finally:
                shutil.rmtree(tempdir)

if __name__ == '__main__':
    unittest.main()

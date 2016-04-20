# coding=utf-8

import os.path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from mock import patch
from devpi_plumber.server import TestServer
from devpi_plumber.client import DevpiClient

from devpi_builder.cli import main
from devpi_builder import wheeler


USER = 'user'
INDEX = 'user/wheels'
PURE_INDEX = 'user/packages'
PASSWORD = 'secret'

USERS = {
    USER: {'password': PASSWORD},
}
INDICES = {
    INDEX: {'bases': ''},
    PURE_INDEX: {'bases': ''},
}


def package_version_exists(client, index, package, version):
    client.use(index)
    spec = "{}=={}".format(package, version)
    packages = client.list(spec)
    return wheeler.has_compatible_wheel(packages)


class CliTest(unittest.TestCase):
    def test_basic(self):
        with TestServer(USERS, INDICES) as devpi:
            main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX, USER, PASSWORD])

            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))

    def test_with_blacklist(self):
        with TestServer(USERS, INDICES) as devpi:

            main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX, USER, PASSWORD, '--blacklist={}'.format('tests/fixture/sample_no_version.txt')])

            self.assertFalse(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'six', '1.7.3'))

    def test_multiple_versions(self):
        with TestServer(USERS, INDICES) as devpi:

            main(['tests/fixture/sample_multiple_versions.txt', devpi.url + '/' + INDEX, USER, PASSWORD])

            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.1'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))

    def test_reupload_is_safe(self):
        with TestServer(USERS, INDICES) as devpi:

            main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX, USER, PASSWORD])
            main(['tests/fixture/sample_multiple_versions.txt', devpi.url + '/' + INDEX, USER, PASSWORD])

            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.1'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'six', '1.7.3'))

    def test_continue_on_failed(self):
        with TestServer(USERS, INDICES) as devpi:

            main(['tests/fixture/sample_continue_on_failed.txt', devpi.url + '/' + INDEX, USER, PASSWORD])

            self.assertTrue(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))

    def test_different_styles(self):
        with TestServer(USERS, INDICES) as devpi:

            main(['tests/fixture/sample_different_styles.txt', devpi.url + '/' + INDEX, USER, PASSWORD])

            self.assertTrue(package_version_exists(devpi, INDEX, 'pygments', '1.6'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'Pygments', '1.6'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'Django', '1.6.5'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'django', '1.6.5'))

    def test_not_built_if_on_pure(self):
        """
        Verify that packages are not built and re-uploaded if they are already on the pure index.
        """
        with TestServer(USERS, INDICES) as devpi:
            with DevpiClient(devpi.server_url + '/' + PURE_INDEX, USER, PASSWORD) as pure_client:
                pure_client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

            with patch.object(wheeler.Builder, 'build', autospec=True, side_effect=Exception('Should not build!')) as mock_build:

                main(['tests/fixture/sample_test_package.txt', devpi.url + '/' + INDEX, USER, PASSWORD, '--pure-index={}'.format(pure_client.url)])

                self.assertFalse(mock_build.called)

    def test_fills_proper_index(self):
        """
        Verify that pure packages are uploaded to the pure index non-pure packages are uploaded to the normal index.
        """
        with TestServer(USERS, INDICES) as devpi:

            main([
                'tests/fixture/sample_pure_and_non-pure.txt',
                devpi.url + '/' + INDEX,
                USER,
                PASSWORD,
                '--pure-index={}'.format(devpi.url + '/' + PURE_INDEX)
            ])

            self.assertTrue(package_version_exists(devpi, PURE_INDEX, 'progressbar', '2.2'))
            self.assertFalse(package_version_exists(devpi, PURE_INDEX, 'PyYAML', '3.10'))

            self.assertFalse(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))
            self.assertTrue(package_version_exists(devpi, INDEX, 'PyYAML', '3.10'))

    def _assert_test_case(self, root_element, result_tag_type, expected_element_name):
        xpath = './/testcase/{}/..'.format(result_tag_type)
        matched_nodes = root_element.findall(xpath)
        self.assertEqual(1, len(matched_nodes))
        self.assertEqual(matched_nodes[0].attrib['name'], expected_element_name)

    def _assert_junit_xml_content(self, junit_filename):
        root = ET.parse(junit_filename)
        ET.dump(root)

        self._assert_test_case(root, 'failure', 'package-that-hopefully-not-exists 99.999')
        self._assert_test_case(root, 'skipped', 'test-package 0.1.dev1')

        pb_elems = root.findall(".//testcase[@name='progressbar 2.2']")
        self.assertEqual(1, len(pb_elems))
        pb_elem = pb_elems[0]
        self.assertIsNone(pb_elem.find('failure'))
        self.assertIsNone(pb_elem.find('error'))
        self.assertIsNone(pb_elem.find('skipped'))

    def test_reports_junit_xml(self):
        with TestServer(USERS, INDICES) as devpi:

            with DevpiClient(devpi.server_url + '/' + INDEX, USER, PASSWORD) as client:
                client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

            tempdir = tempfile.mkdtemp()
            try:
                junit_filename = os.path.join(tempdir, 'junit.xml')
                main(['tests/fixture/sample_junit.txt', devpi.url + '/' + INDEX, USER, PASSWORD, '--junit-xml', junit_filename])

                self._assert_junit_xml_content(junit_filename)
            finally:
                shutil.rmtree(tempdir)

    def test_dry_run(self):
        """
        Test that a dry run produces the same ``junit.xml`` as a run without dry-run but does not modify the server
        state.
        """
        with TestServer(USERS, INDICES) as devpi:
            with DevpiClient(devpi.server_url + '/' + INDEX, USER, PASSWORD) as client:
                client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

            tempdir = tempfile.mkdtemp()
            try:
                junit_filename = os.path.join(tempdir, 'junit.xml')
                main([
                    'tests/fixture/sample_junit.txt',
                    devpi.url + '/' + INDEX,
                    USER,
                    PASSWORD,
                    '--junit-xml', junit_filename,
                    '--dry-run',
                ])

                self._assert_junit_xml_content(junit_filename)
            finally:
                shutil.rmtree(tempdir)

            self.assertFalse(package_version_exists(devpi, INDEX, 'progressbar', '2.2'))

    def test_passes_client_cert(self):
        """
        Verify that packages are not built and re-uploaded if they are already on the pure index.
        """
        PURE_INDEX='pure_index'
        with patch('devpi_builder.cli.DevpiClient') as client:
            main(['tests/fixture/sample_test_package.txt', INDEX, USER, PASSWORD, '--pure-index={}'.format(PURE_INDEX),
                  '--client-cert=some.crt'])

            client.assert_any_call(INDEX, USER, PASSWORD, client_cert='some.crt')
            client.assert_any_call(PURE_INDEX, USER, PASSWORD, client_cert='some.crt')
            self.assertEqual(2, len(client.call_args_list))  # Check that no further instances have been created

if __name__ == '__main__':
    unittest.main()

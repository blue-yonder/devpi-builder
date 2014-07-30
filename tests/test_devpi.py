__author__ = 'mbach'

import unittest

from devpi_builder import devpi

from tests.tools import devpi_server


class TestClient(unittest.TestCase):

    def test_check_for_package_version(self):
        with devpi_server() as server_url:
            devpi_client = devpi.Client(server_url + '/root/pypi')
            self.assert_(devpi_client.package_version_exists('progressbar', '2.2'))
            self.assertFalse(devpi_client.package_version_exists('invalid_package_name', '14.234'))


if __name__ == '__main__':
    unittest.main()

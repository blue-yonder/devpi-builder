__author__ = 'mbach'

import unittest

from brandon.cli import main
from brandon import devpi

from tests.tools import devpi_server, devpi_index


class CliTest(unittest.TestCase):
    @unittest.skip('not implemented')
    def test_basic(self):
        with devpi_server() as server_url, devpi_index(server_url, 'test', 'wheels') as (destination_index, password):
            main(['tests/sample_simple.txt'])

            devpi_client = devpi.Client(destination_index)
            self.assert_(devpi_client.package_version_exists('progressbar', '2.3'))


if __name__ == '__main__':
    unittest.main()

# coding=utf-8

__author__ = 'mbach'

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
                self.assert_(devpi_client.package_version_exists('progressbar', '2.2'))


if __name__ == '__main__':
    unittest.main()

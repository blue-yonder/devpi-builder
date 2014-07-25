__author__ = 'mbach'

import contextlib
import shutil
import subprocess
import tempfile
import unittest

from brandon import devpi


@contextlib.contextmanager
def devpi_server(port=2414):
    server_dir = tempfile.mkdtemp()
    try:
        subprocess.check_call(['devpi-server', '--start', '--serverdir={}'.format(server_dir), '--port={}'.format(port)])
        try:
            yield 'http://localhost:{}'.format(port)
        finally:
            subprocess.check_call(['devpi-server', '--stop', '--serverdir={}'.format(server_dir)])
    finally:
        shutil.rmtree(server_dir)


class TestClient(unittest.TestCase):

    def test_check_for_package_version(self):
        with devpi_server() as server_url:
            devpi_client = devpi.Client(server_url + '/root/pypi')
            self.assert_(devpi_client.package_version_exists('progressbar', '2.2'))
            self.assertFalse(devpi_client.package_version_exists('invalid_package_name', '14.234'))


if __name__ == '__main__':
    unittest.main()

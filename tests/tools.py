"""
Test tools required by multiple suites.
"""

__author__ = 'mbach'


import contextlib
import shutil
import subprocess
import tempfile


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

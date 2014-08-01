# coding=utf-8

"""
Test tools required by multiple suites.
"""

import contextlib
import shutil
import subprocess
import tempfile

from devpi_builder import devpi


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


@contextlib.contextmanager
def devpi_index(server_url, user, index):
    """
    Creates the given user and index, and cleans it afterwards.

    Yields of tuple of index-url and password. The index is created without an upstream.
    """
    password = 'foo'
    with devpi.Client(server_url) as devpi_client:
        devpi_client._execute('user', '-c', user, 'password=' + password)
        devpi_client._execute('login', user, '--password=' + password)
        devpi_client._execute('index', '-c', 'wheels', 'bases=')

        yield '{}/{}/{}'.format(server_url, user, index), password

        devpi_client._execute('index', '--delete', '/{}/{}'.format(user, index))
        devpi_client._execute('user', user, '--delete')

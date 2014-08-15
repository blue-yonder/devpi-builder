# coding=utf-8

"""
Functionality for interacting with a devpi instance.
"""

import subprocess
import tempfile
import shutil
import locale


class Client(object):
    """
    Wrapper object around the devpi client exposing features required by devpi_builder.
    """
    def __init__(self, index_url, user=None, password=None):
        self._index_url = index_url
        self._user = user
        self._password = password

    def __enter__(self):
        self._client_dir = tempfile.mkdtemp()
        self._execute('use', self._index_url)
        if self._user and self._password is not None:
            self._execute('login', self._user, '--password', self._password)
        return self

    def __exit__(self, *args):
        shutil.rmtree(self._client_dir)

    def _execute(self, *args):
        return subprocess.check_output(
            ['devpi'] + list(args) + ['--clientdir={}'.format(self._client_dir)],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

    def package_version_exists(self, package, version):
        """
        Check whether the given version of the given package is in the index of this client.

        :param package: Python package to check for
        :param version: Version of the package to check for (string)
        :return: True if the exact version of this package is in the index, else False.
        """
        try:
            return "" != self._execute('list', '{}=={}'.format(package, version))
        except subprocess.CalledProcessError as e:
            if '404' in e.output:
                return False  # package does not exist
            else:
                raise e

    def upload(self, file):
        """
        Upload the given file to the current index
        """
        self._execute('upload', file)

    @property
    def index_url(self):
        return self._index_url

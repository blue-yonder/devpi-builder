"""
Functionality for interacting with a devpi instance.
"""

import subprocess
import tempfile
import shutil

__author__ = 'mbach'


class Client(object):
    """
    Wrapper object around the devpi client exposing features required by devpi_builder.
    """
    def _execute(self, *args):
        return subprocess.check_output(['devpi', '--clientdir={}'.format(self._client_dir)] + list(args))

    def __init__(self, index_url):
        self._index_url = index_url

    def __enter__(self):
        self._client_dir = tempfile.mkdtemp()
        self._execute('use', self._index_url)
        return self

    def __exit__(self, *args):
        shutil.rmtree(self._client_dir)

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
                # package does not exist
                return False
            else:
                raise

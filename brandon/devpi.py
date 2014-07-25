"""
Functionality for interacting with a devpi instance.
"""

import subprocess
import tempfile

__author__ = 'mbach'


class Client(object):

    def _execute(self, *args):
        return subprocess.check_output(['devpi', '--clientdir={}'.format(self.client_dir)] + list(args))

    def __init__(self, index_url):
        self.client_dir = tempfile.mkdtemp()
        self._execute('use', index_url)

    def package_version_exists(self, package, version):
        try:
            return "" != self._execute('list', '{}=={}'.format(package, version))
        except subprocess.CalledProcessError as e:
            if '404' in e.output:
                # package does not exist
                return False
            else:
                raise
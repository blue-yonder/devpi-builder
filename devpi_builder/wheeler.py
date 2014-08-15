# coding=utf-8

"""
Functionality for building wheels
"""

import glob
import os.path as path
import shutil
import subprocess
import tempfile

import wheel.install
import wheel.util


class BuildError(Exception):
    def __init__(self, package, version, root_exception=None):
        super(BuildError, self).__init__('Failed to create wheel for {} {}:\n{}\nOutput:\n{}'.format(
            package,
            version,
            root_exception,
            root_exception.output if hasattr(root_exception, 'output') and root_exception.output else ''
        ))


class Builder(object):
    """
    Provides a context in which wheels can be generated. If the context goes out of scope all created files will be
    removed.
    """

    def __enter__(self):
        self.scratch_dir = tempfile.mkdtemp()
        self.wheelhouse = path.join(self.scratch_dir, 'wheels')
        self.builddir = path.join(self.scratch_dir, 'build')
        self.cachedir = path.join(self.scratch_dir, 'cache')
        return lambda *args: self.build(*args)

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.scratch_dir)

    def _find_wheel(self, name, version):
        """
        Find a wheel with the given name and version
        """
        candidates = [
            wheel.install.WheelFile(filename) for filename in glob.glob(path.join(self.wheelhouse, '*.whl'))
        ]
        matches = wheel.util.matches_requirement('{}=={}'.format(name, version), candidates)
        if len(matches) > 0:
            return str(matches[0])
        else:
            raise BuildError(name, version, 'Failed to find the build wheel for {} {}'.format(name, version))

    def build(self, package, version):
        """
        Build a wheel for the given version of the given project.

        :param package: The name of the project
        :param version: The version to generate the wheel for
        :return: The path of the build wheel. Valid until the context is exited.
        """
        shutil.rmtree(self.builddir, ignore_errors=True)
        try:
            subprocess.check_output([
                'pip', 'wheel',
                '--wheel-dir=' + self.wheelhouse,
                '--download-cache=' + self.cachedir,
                '--build=' + self.builddir,
                '{}=={}'.format(package, version)
            ])
            return self._find_wheel(package, version)
        except subprocess.CalledProcessError as e:
            raise BuildError(package, version, e)


def is_pure(path):
    """
    Check whether wheel given by the passed path is pure.

    Pure wheels operate independent of the specific Python version and platform.

    :param path: The path to the wheel to inspect
    :return: True if the wheel is pure
    """
    wheel_file = wheel.install.WheelFile(path)
    return wheel_file.parsed_wheel_info['Root-Is-Purelib'] == 'true'  # safe default

# coding=utf-8

"""
Functionality for building wheels
"""

import glob
import os.path as path
import shutil
import subprocess
import tempfile

from wheel.install import WheelFile, BadWheelFile
from wheel.util import matches_requirement


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
    Provides a context in which wheels can be generated. If the context goes out of scope
    all created files will be removed.
    """
    def __enter__(self):
        self.scratch_dir = tempfile.mkdtemp()
        self.wheelhouse = path.join(self.scratch_dir, 'wheels')
        self.builddir = path.join(self.scratch_dir, 'build')
        return lambda *args: self.build(*args)

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.scratch_dir)

    def _find_wheel(self, name, version):
        """
        Find a wheel with the given name and version
        """
        candidates = [WheelFile(filename) for filename in glob.iglob(path.join(self.wheelhouse, '*.whl'))]
        matches = matches_requirement('{}=={}'.format(name, version), candidates)
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
                '--build=' + self.builddir,
                '{}=={}'.format(package, version)
            ], stderr=subprocess.STDOUT)
            return self._find_wheel(package, version)
        except subprocess.CalledProcessError as e:
            raise BuildError(package, version, e)


def is_pure(wheel):
    """
    Check whether wheel given by the passed path is pure.

    Pure wheels operate independent of the specific Python version and platform.

    :param wheel: The path to the wheel to inspect
    :return: True if the wheel is pure
    """
    return WheelFile(wheel).parsed_wheel_info['Root-Is-Purelib'] == 'true'  # safe default


def is_compatible(package):
    """
    Check whether the given python package is a wheel compatible with the
    current platform and python interpreter.
    """
    try:
        return WheelFile(package).compatible
    except BadWheelFile:
        return False


def has_compatible_wheel(packages):
    """
    Check for a compatible wheel in the given list of python packages
    """
    return any(is_compatible(pkg) for pkg in packages)

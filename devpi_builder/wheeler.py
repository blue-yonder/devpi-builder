# coding=utf-8

"""
Functionality for building wheels
"""

import glob
import os.path as path
import shutil
import subprocess
import tempfile

from packaging import tags
from pkg_resources import Distribution, Requirement

from wheel_filename import InvalidFilenameError, parse_wheel_filename
from wheel_inspect import inspect_wheel
from wheel_inspect.classes import WheelFile

class BuildError(Exception):
    def __init__(self, package, version, root_exception=None):
        version = version or ""
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
        return lambda *args: self.build(*args)

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.scratch_dir)

    @staticmethod
    def _standardize_package_name(name):
        return name.replace(".", "-")

    def _matches_requirement(self, requirement, wheels):
        """
        List wheels matching a requirement.

        :param requirement:str : The requirement to satisfy
        :param wheels: List of wheels to search.
        """
        req = Requirement.parse(requirement)

        matching = []
        for wheel in wheels:
            w = wheel.parsed_filename
            dist = Distribution(project_name=self._standardize_package_name(w.project), version=w.version)
            if dist in req:
                matching.append(wheel.path)
        return matching


    def _find_wheel(self, name, version):
        """
        Find a wheel with the given name and version
        """
        candidates = [WheelFile(filename) for filename in glob.iglob(path.join(self.wheelhouse, '*.whl'))]
        name = self._standardize_package_name(name)
        requirement = '{}=={}'.format(name, version) if version else name
        matches = self._matches_requirement(requirement, candidates)
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
        try:
            subprocess.check_output([
                'pip', 'wheel',
                '--wheel-dir=' + self.wheelhouse,
                '{}=={}'.format(package, version) if version else package,
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
    return (
        inspect_wheel(wheel)
            .get("dist_info", {})
            .get("wheel", {})
            .get("root_is_purelib")
    )


def is_compatible(package):
    """
    Check whether the given python package is a wheel compatible with the
    current platform and python interpreter.

    Compatibility is based on https://www.python.org/dev/peps/pep-0425/
    """
    try:
        w = parse_wheel_filename(package)
        for systag in tags.sys_tags():
            for tag in w.tag_triples():
                if systag in tags.parse_tag(tag):
                    return True
    except InvalidFilenameError:
        return False


def has_compatible_wheel(packages):
    """
    Check for a compatible wheel in the given list of python packages
    """
    return any(is_compatible(pkg) for pkg in packages)

# coding=utf-8

"""
Functionality for reading specifications of required packages.
"""

import pkg_resources


def _extract_project_version(requirement):
    """
    Extract the information on a concrete project version from pkg_configs Requirement information.

    :param requirement: A pkg_config Requirement
    :return: Pair of project_name and version
    """
    specs = requirement.specs
    if len(specs) == 1:
        spec = specs[0]
        if spec[0] == '==':
            return requirement.project_name, spec[1]
        else:
            raise ValueError('Versions must be specified exactly. "{}" is not an exact version specification.'.format(requirement))
    elif len(specs) > 1:
        raise ValueError('Multiple version specifications on a single line are not supported.')
    else:
        raise ValueError('Version specification is missing for "{}".'.format(requirement))


def read_raw(filename):
    if filename:
        with open(filename) as requirements_file:
            return list(pkg_resources.parse_requirements(requirements_file))
    else:
        return []


def read_exact_versions(filename):
    """
    Read the list of requested software.

    Multiple versions may be specified for a project, however each project must have an exact (==) version specified.

    :param filename: Filename of the requirements-style file.
    :return: A list of package-version pairs.
    """
    return [
        _extract_project_version(requirement) for requirement in read_raw(filename)
    ]


def matched_by_list(package, version, requirements):
    """
    Verify whether the given version of the package is matched by the given requirements file.

    :param package: Name of the package to look for
    :param version: Version of the package to look for
    :param requirements: A list of requirements as read by read_raw()
    :return: True if the package can be used to fulfil on of the requirements in the file, False otherwise
    """
    version = pkg_resources.safe_version('{}'.format(version))
    package = pkg_resources.safe_name(package)
    matches = (
        package == requirement.project_name and version in requirement
        for requirement in requirements
    )
    return any(matches)

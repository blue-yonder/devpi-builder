# coding=utf-8

"""
Functionality for reading specifications of required packages.
"""

import pip_requirements_parser
import pkg_resources


def _extract_project_version(requirement):
    """
    Extract the information on a concrete project version from pkg_configs Requirement information.

    :param requirement: A pkg_config Requirement
    :return: Pair of project_name and version
    """
    if requirement.is_vcs_url:
        return requirement.line, None
    if not requirement.specifier:
        raise ValueError('Version specification is missing for "{}".'.format(requirement.line))
    else:
        if len(requirement.specifier) == 1 and requirement.is_pinned:
            return requirement.name, requirement.get_pinned_version
        elif len(requirement.specifier) == 1 and not requirement.is_pinned:
            raise ValueError('Versions must be specified exactly. "{}" is not an exact version specification.'.format(requirement.line))
        elif len(requirement.specifier) > 1:
            raise ValueError('Multiple version specifications on a single line are not supported.')


def read_raw(filename):
    if filename:
        rf = pip_requirements_parser.RequirementsFile.from_file(filename)
        if rf.invalid_lines:
            raise ValueError("There are invalid lines in requirements file: \n", "\n".join(line.dumps() for line in rf.invalid_lines))
        return rf.requirements
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
        package.lower() == pkg_resources.safe_name(requirement.name) and (requirement.specifier.contains(version) if requirement.specifier else 1)
        for requirement in requirements
    )
    return any(matches)

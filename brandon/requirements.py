"""
Functionality for reading specifications of required packages.
"""

import pkg_resources

__author__ = 'mbach'

def read(filename):
    """
    Read the list of requested software.

    Multiple versions may be specified for a project, however each project must have an exact (==) version specified.

    :param filename: Filename of the requirements style file.
    :return: A list of package-version pairs.
    """
    with open(filename) as input_file:
        return [
            (requirement.project_name, requirement.specs[0][1]) for requirement in pkg_resources.parse_requirements(input_file)
        ]
"""
Command line interface for brandon
"""

import argparse

from devpi_builder import requirements, wheeler, devpi


__author__ = 'mbach'


def main(args=None):
    parser = argparse.ArgumentParser(description='Create wheels for all given project versions and upload them to the given index.')
    parser.add_argument('requirements', help='requirements.txt style file specifying which project versions to package.')
    parser.add_argument('index', help='The index to upload the packaged software to.')

    args = parser.parse_args(args=args)

    with wheeler.Builder() as builder:
        for (package, version) in requirements.read(args.requirements):
            print 'Building {} {}'.format(package, version)
            wheel_file = builder(package, version)

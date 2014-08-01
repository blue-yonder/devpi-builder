# coding=utf-8

"""
Command line interface for brandon
"""

import argparse
import logging

from devpi_builder import requirements, wheeler, devpi

logging.basicConfig()
logger = logging.getLogger(__name__)


def main(args=None):
    parser = argparse.ArgumentParser(description='Create wheels for all given project versions and upload them to the given index.')
    parser.add_argument('requirements', help='requirements.txt style file specifying which project versions to package.')
    parser.add_argument('index', help='The index to upload the packaged software to.')
    parser.add_argument('user', help='The user to log in as.')
    parser.add_argument('password', help='Password of the user.')
    parser.add_argument('--blacklist', help='Packages matched by this requirements.txt style file will never be build.')

    args = parser.parse_args(args=args)

    with wheeler.Builder() as builder, devpi.Client(args.index, args.user, args.password) as devpi_client:
        for package, version in requirements.read(args.requirements):

            if devpi_client.package_version_exists(package, version):
                logger.debug('Skipping %s %s as is already available on the index.', package, version)
            elif args.blacklist and requirements.matched_by_file(package, version, args.blacklist):
                logger.info('Skipping %s %s as it is matched by the blacklist.', package, version)
            else:
                logger.info('Building %s %s', package, version)
                try:
                    wheel_file = builder(package, version)
                    devpi_client.upload(wheel_file)
                except wheeler.BuildError as e:
                    logger.exception(e)

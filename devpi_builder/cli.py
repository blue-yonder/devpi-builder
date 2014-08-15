# coding=utf-8

"""
Command line interface for brandon
"""

import argparse
import logging

from devpi_builder import requirements, wheeler, devpi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_packages(packages, builder, devpi_client, blacklist, pure_index_client=None):
    for package, version in packages:
        if devpi_client.package_version_exists(package, version):
            logger.debug('Skipping %s %s as is already available on the index.', package, version)
        elif pure_index_client and pure_index_client.package_version_exists(package, version):
            logger.debug('Skipping %s %s as is already available on the pure index.', package, version)
        elif blacklist and requirements.matched_by_file(package, version, blacklist):
            logger.info('Skipping %s %s as it is matched by the blacklist.', package, version)
        else:
            logger.info('Building %s %s', package, version)
            try:
                wheel_file = builder(package, version)
                if pure_index_client and wheeler.is_pure(wheel_file):
                    logger.debug('Uploading %s %s to pure index %s', package, version, pure_index_client.index_url)
                    pure_index_client.upload(wheel_file)
                else:
                    logger.debug('Uploading %s %s to %s', package, version, devpi_client.index_url)
                    devpi_client.upload(wheel_file)
            except wheeler.BuildError as e:
                logger.exception(e)


def main(args=None):
    parser = argparse.ArgumentParser(description='Create wheels for all given project versions and upload them to the given index.')
    parser.add_argument('requirements', help='requirements.txt style file specifying which project versions to package.')
    parser.add_argument('index', help='The index to upload the packaged software to.')
    parser.add_argument('user', help='The user to log in as.')
    parser.add_argument('password', help='Password of the user.')
    parser.add_argument('--blacklist', help='Packages matched by this requirements.txt style file will never be build.')
    parser.add_argument('--pure-index', help='The index to use for pure packages. Any non-pure package will be uploaded'
                                             'to the index given as positional argument. Packages already found in the'
                                             'pure index will not be built, either.'
    )

    args = parser.parse_args(args=args)

    packages = requirements.read(args.requirements)
    with wheeler.Builder() as builder, devpi.Client(args.index, args.user, args.password) as devpi_client:
        if args.pure_index:
            with devpi.Client(args.pure_index, args.user, args.password) as pure_index_client:
                build_packages(packages, builder, devpi_client, args.blacklist, pure_index_client)
        else:
            build_packages(packages, builder, devpi_client, args.blacklist)

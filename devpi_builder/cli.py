# coding=utf-8

"""
Command line interface for brandon
"""

import argparse
import logging

from junit_xml import TestSuite, TestCase
from devpi_plumber.client import DevpiClient

from devpi_builder import requirements, wheeler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Processor(object):

    def __init__(self, builder, devpi_client, blacklist, pure_index_client=None, junit_xml=None, dry_run=False):
        self._builder = builder
        self._devpi_client = devpi_client
        self._blacklist = blacklist
        self._pure_index_client = pure_index_client
        self._junit_xml = junit_xml
        self._dry_run = dry_run
        self._results = []

    def _log_skip(self, text, package, version):
        logger.debug(text, package, version)

        log_entry = TestCase('{} {}'.format(package, version))
        log_entry.add_skipped_info(text % (package, version))
        self._results.append(log_entry)

    def _log_fail(self, exception, package, version):
        logger.exception(exception)

        log_entry = TestCase('{} {}'.format(package, version))
        log_entry.add_failure_info(str(exception))
        self._results.append(log_entry)

    def _log_success(self, package, version):
        log_entry = TestCase('{} {}'.format(package, version))
        self._results.append(log_entry)

    def _should_package_be_build(self, package, version):
        spec = "{}=={}".format(package, version)

        if self._blacklist and requirements.matched_by_file(package, version, self._blacklist):
            self._log_skip('Skipping %s %s as it is matched by the blacklist.', package, version)
            return False
        elif wheeler.has_compatible_wheel(self._devpi_client.list(spec)):
            self._log_skip('Skipping %s %s as is already available on the index.', package, version)
            return False
        elif self._pure_index_client and wheeler.has_compatible_wheel(self._pure_index_client.list(spec)):
            self._log_skip('Skipping %s %s as is already available on the pure index.', package, version)
            return False
        return True

    def _upload_package(self, package, version, wheel_file):
        if self._pure_index_client and wheeler.is_pure(wheel_file):
            logger.debug('Uploading %s %s to pure index %s', package, version, self._pure_index_client.url)
            self._pure_index_client.upload(wheel_file, dry_run=self._dry_run)
        else:
            logger.debug('Uploading %s %s to %s', package, version, self._devpi_client.url)
            self._devpi_client.upload(wheel_file, dry_run=self._dry_run)

    def build_packages(self, packages):
        self._results = []

        for package, version in packages:
            if self._should_package_be_build(package, version):
                logger.info('Building %s %s', package, version)
                try:
                    wheel_file = self._builder(package, version)
                    self._upload_package(package, version, wheel_file)
                    self._log_success(package, version)
                except wheeler.BuildError as e:
                    self._log_fail(e, package, version)

        if self._junit_xml:
            with open(self._junit_xml, 'w') as output:
                test_suite = TestSuite('devpi-builder results', self._results)
                TestSuite.to_file(output, [test_suite])


def main(args=None):
    parser = argparse.ArgumentParser(description='Create wheels for all given project versions and upload them to the given index.')
    parser.add_argument('requirements', help='requirements.txt style file specifying which project versions to package.')
    parser.add_argument('index', help='The index to upload the packaged software to.')
    parser.add_argument('user', help='The user to log in as.')
    parser.add_argument('password', help='Password of the user.')
    parser.add_argument('--blacklist', help='Packages matched by this requirements.txt style file will never be build.')
    parser.add_argument('--pure-index', help='The index to use for pure packages. Any non-pure package will be uploaded '
                                             'to the index given as positional argument. Packages already found in the '
                                             'pure index will not be built, either.'
    )
    parser.add_argument('--junit-xml', help='Write information about the build success / failure to a JUnit-compatible XML file.')
    parser.add_argument('--dry-run', help='Build missing wheels, but do not modify the state of the devpi server.', action='store_true')
    parser.add_argument('--client-cert', help='Client key to use to authenticate with the devpi server.', default=None)

    args = parser.parse_args(args=args)

    packages = requirements.read(args.requirements)
    with wheeler.Builder() as builder, DevpiClient(args.index, args.user, args.password, client_cert=args.client_cert) as devpi_client:
        if args.pure_index:
            with DevpiClient(args.pure_index, args.user, args.password, client_cert=args.client_cert) as pure_index_client:
                processor = Processor(builder, devpi_client, args.blacklist, pure_index_client, junit_xml=args.junit_xml, dry_run=args.dry_run)
                processor.build_packages(packages)
        else:
            processor = Processor(builder, devpi_client, args.blacklist, junit_xml=args.junit_xml, dry_run=args.dry_run)
            processor.build_packages(packages)

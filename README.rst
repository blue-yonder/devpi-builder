=========================
Brandon the Devpi Builder
=========================

.. image:: https://travis-ci.org/blue-yonder/devpi-builder.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/blue-yonder/devpi-builder
.. image:: https://coveralls.io/repos/blue-yonder/devpi-builder/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/blue-yonder/devpi-builder?branch=master
.. image:: https://badge.fury.io/py/devpi-builder.svg
    :alt: Latest Version
    :target: https://pypi.python.org/pypi/devpi-builder

Brandon, the devpi builder, takes a ``requirements.txt`` and incrementally fills a devpi_ index with wheels of the listed python packages.


Brandon by Example
==================

Given a ``requirements.txt``, we can upload all listed packages to the index ``opensource/Debian_7`` on a local devpi using the following command::

    $ devpi-builder requirements.txt http://localhost:3141/opensource/Debian_7

Example of such a ``requirements.txt``::

    progressbar==0.2.2
    progressbar==0.2.1
    PyYAML==3.11

Commandline Usage
=================
::

    usage: devpi-builder [-h] [--batch] [--user USER] [--password PASSWORD]
                        [--blacklist BLACKLIST] [--pure-index PURE_INDEX]
                        [--junit-xml JUNIT_XML] [--run-id RUN_ID] [--dry-run]
                        [--client-cert CLIENT_CERT]
                        requirements index

    Create wheels for all given project versions and upload them to the given
    index.

    positional arguments:
    requirements          requirements.txt style file specifying which project
                            versions to package.
    index                 The index to upload the packaged software to.

    optional arguments:
    -h, --help            show this help message and exit
    --batch               Batch mode. Do not prompt for credentials
    --user USER           The user to log in as.
    --password PASSWORD   Password of the user.
    --blacklist BLACKLIST
                            Packages matched by this requirements.txt style file
                            will never be build.
    --pure-index PURE_INDEX
                            The index to use for pure packages. Any non-pure
                            package will be uploaded to the index given as
                            positional argument. Packages already found in the
                            pure index will not be built, either.
    --junit-xml JUNIT_XML
                            Write information about the build success / failure to
                            a JUnit-compatible XML file.
    --run-id RUN_ID       Add the given string to all entries in the XML output,
                            allowing to distinguish output from multiple runs in a
                            merged XML.
    --dry-run             Build missing wheels, but do not modify the state of
                            the devpi server.
    --client-cert CLIENT_CERT
                            Client key to use to authenticate with the devpi
                            server.

The following environment variables can be used instead of command line arguments:

``DEPVI_USER``
    The value of this environment variable will be used if ``--user`` is not given.

``DEVPI_PASSWORD``
    The value of this environment variable will be used if ``--password`` is not given.

Features
========

* Read a ``requirements.txt`` style input file.
* Read user/pass from environment (using DEVPI_USER/DEVPI_PASS)
* Support multiple versions of a package in the same file
* Only build packages not yet in the target index.
* Support a black-list for packages to never be built and uploaded (certain packages like numpy are fragile regarding their interdependency with other packages).
* Can use separate indices for plain python packages and those with binary contents.
* Can log build results to a JUnit compatible XML file, thus that it can be parsed by Jenkins.


License
=======

`New BSD`_


.. _devpi: http://doc.devpi.net/latest/
.. _New BSD: https://github.com/blue-yonder/devpi-builder/blob/master/COPYING

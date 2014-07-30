Brandon the Devpi Builder
=========================
[![Build Status](https://travis-ci.org/blue-yonder/devpi-builder.svg?branch=master)](https://travis-ci.org/blue-yonder/devpi-builder)
[![Coverage Status](https://coveralls.io/repos/blue-yonder/devpi-builder/badge.png?branch=master)](https://coveralls.io/r/blue-yonder/devpi-builder?branch=master)
[![Requirements Status](https://requires.io/github/blue-yonder/devpi-builder/requirements.png?branch=master)](https://requires.io/github/blue-yonder/devpi-builder/requirements/?branch=master)

This tools takes a list of python packages, specified as in an `requirements.txt` and incrementally fills a
[devpi](http://doc.devpi.net/latest/) index with them.

Usage:

    devpi-builder --help
    usage: devpi-builder [-h] requirements index user password

    Create wheels for all given project versions and upload them to the given index.

    positional arguments:
        requirements  requirements.txt style file specifying which project versions to package.
        index         The index to upload the packaged software to.
        user          The user to log in as.
        password      Password of the user.


Example requirements textfile:

    progressbar==0.2.2
    progressbar==0.2.1 
    six==1.7.3


Features
--------

 * Reads a `requirements.txt` stile input file.
 * Multiple versions of a package may be imported in the same file
 * Only builds packages not yet in the target index.


Planned
-------
 * Supports a black-list for packages to never be built and uploaded (certain packages like numpy are fragile regarding
   their interdependency with other packages).
 * Support extras
 * Can use separate indices for plain python packages and those with binary contents.
    - Optionally only operates on one of the two.


License
-------

New BSD

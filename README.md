Brandon the Devpi Builder
=========================
[![Build Status](https://travis-ci.org/blue-yonder/devpi-builder.svg?branch=master)](https://travis-ci.org/blue-yonder/devpi-builder)
[![Coverage Status](https://coveralls.io/repos/blue-yonder/devpi-builder/badge.png?branch=master)](https://coveralls.io/r/blue-yonder/devpi-builder?branch=master)
[![Requirements Status](https://requires.io/github/blue-yonder/devpi-builder/requirements.png?branch=master)](https://requires.io/github/blue-yonder/devpi-builder/requirements/?branch=master)

Brando, the devpi-builder, takes a `requirements.txt` and incrementally fills a [devpi](http://doc.devpi.net/latest/) index with wheels of the listed python packages.


Brandon by Example:
-------------------

Given a `requirements.txt`, we can upload all listed packages to the index `opensource/Debian_7` using the following command:

    $ devpi-builder requirements.txt opensource/Debian_7 opensource mypassword
    
Example of such a requirements.txt:

    progressbar==0.2.2 
    progressbar==0.2.1 
    PyYAML==3.11

Commandline Usage
-----------------

    usage: devpi-builder [-h] [--blacklist BLACKLIST]
                         requirements index user password
    
    Create wheels for all given project versions and upload them to the given
    index.
    
    positional arguments:
      requirements          requirements.txt style file specifying which project
                            versions to package.
      index                 The index to upload the packaged software to.
      user                  The user to log in as.
      password              Password of the user.
    
    optional arguments:
      -h, --help            show this help message and exit
      --blacklist BLACKLIST
                            Packages matched by this requirements.txt style file
                            will never be build.


Feaures & Backlog
------------------

 * [x] Read a `requirements.txt` stile input file.
 * [x] Support multiple versions of a package in the same file 
 * [x] Only build packages not yet in the target index.
 * [x] Support a black-list for packages to never be built and uploaded (certain packages like numpy are fragile regarding their interdependency with other packages).
 * [ ] Support extras requirements of packages
 * [ ] Can use separate indices for plain python packages and those with binary contents. Optionally only operates on one of the two.


License
-------

[New BSD](COPYING)

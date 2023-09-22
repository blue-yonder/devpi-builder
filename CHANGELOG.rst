=========
Changelog
=========

This lists the most important changes for each release.


Version 6.1.0 — 2023-09-22
==========================

Added
-----

* Support using VCS URLs in requirements files.

Fixed
-----

* Building wheels for packages like ``zope-event`` that normalise the project name using dots instead of underscores is no longer broken.


Version 6.0.0 — 2023-06-09
==========================

Added
-----

* Python 3.10 and 3.11 are now supported.

Changed
-------

* Improved performance of checking for already built packages.

Removed
-------

* Dropped support for running tests via `setup.py test`.
  The mechanism is considered deprecated by upstream and removing it allows us to drop a dependency.
* Python 3.6 is no longer supported. It likely still works but we will no longer run CI against it.


Version 5.1.0 — 2021-11-05
==========================

Added
-----

* Provide compatibility with pip 21.3 and above which drops the `--build-directory` option.
  Pip has been using a temporary directory for builds since version 1.2 so manual handling of this directory should not be necessary anymore.


Version 5.0.1 – 2020-09-09
==========================

Fixed
-----

* Adhere to case-insensivity when comparing package names.
  This will lead to blacklisting 'cython' vs. 'Cython' being the same thing.


Version 5.0.0 – 2020-04-24
==========================

Fixed
-----

* Remove dependency on the internal ``wheel`` API.
  This blocked the use of ``wheel`` versions >= 0.32.

Removed
-------

* Python 2 is no longer supported.
* Python 3.5 is no longer supported.


Version 4.0.0 – 2018-11-02
==========================

Fixed
-----

* Correctly specify the dependency to Wheel to avoid the latest, incompatible versions.

Removed
-------

* Python 3.3 and Python 3.4 are no longer supported.


Version 3.0.1 — 2017-11-21
==========================

Fixed
-----

* Properly handle non-ASCII characters in the output of failed package builds. Previous versions used to crash in this
  case if a JUnit XML output file was requested.

Version 3.0.0 — 2017-06-16
==========================

Added
-----

* The command line parameter ``--batch`` can be used to disable any prompts.

Changed
-------

* The way credentials are passed has been changed in an incompatible way.
  The positional arguments for user and password no longer exist.
  Instead, use one of the following:

  - Pass the credentials via ``--user`` and ``--password`` command line arguments.
  - Pass the credentials via the environment variables ``DEVPI_USER`` and ``DEVPI_PASSWORD``.
  - Answer the interactive prompt for user and password. This is only possible if ``--batch`` is not used.


Version 2.3.1 — 2017-05-19
==========================

Changed
-------

* Improved performance if a blacklist is used.


Version 2.3.0 — 2017-04-07
==========================

Added
-----

* The command line parameter ``--run-id`` allows to specify a run identifier that will be added to each entry in the
  generated JUnit XML.

Changed
-------

* Changelog is now in the format suggested by Keep-a-CHANGELOG_.


Version 2.2.0 — 2016-05-23
==========================

Added
-----

* Capture build errors for better output in case of build failures. Thanks Travis Mehlinger.


Version 2.1.0 — 2016-04-22
==========================

Added
-----

* Support for client certificates. Thanks Hans Lawrenz.


Version 2.0.0 — 2016-01-20
==========================

Added
-----

* Compatibility with pip >= 8.0 by relying on pip's default download cache
  mechanism instead of explicitly requiring a download cache. This effectively
  disables caching for people still using pip < 6.0.
  Thanks Christian Stefanescu.
* Support for dry-running the wheel build without changing the devpi server state.
* Python 3.5 is now officially supported.

Removed
-------

* Python 3.2 is no longer supported.


Version 1.0.0 — 2015-05-22
==========================

Changed
-------

- Use devpi-plumber_ instead of a custom devpi wrapper.
- Check the blacklist first when deciding whether to build a package.

Version 0.4.0 — 2015-09-13
==========================

Changed
-------

* Only consider a package to exist if it is a wheel and it is compatible with
  the current system. Thanks Michael Still and David Szotten

Fixed
-----

* The source distribution now properly contains a README.md.
  Thanks Mikhail Lukyanchenko.


Version 0.3.0 — 2015-08-15
==========================

Added
-----

* Support for special-case handling of pure python wheels
* Optional support for reporting skipped packages in a JUnit-compatible XML
* Python 3 support


Version 0.2.1 — 2014-08-07
==========================

Fixed
-----

* Fixed crash if a built wheel could cannot be found
  (because pip<=1.5.2 skipped it).


Version 0.2.0 — 2014-08-01
==========================

Added
-----

* Support for package blacklisting to never build certain wheels.

Changed
-------

* build as many packages as possible. Do not stop if one fails.


Version 0.1.0 — 2014-08-01
==========================

Added
-----

- Build a list of packages and upload them to a Devpi index


.. _devpi-plumber: https://github.com/blue-yonder/devpi-plumber
.. _Keep-a-CHANGELOG: http://keepachangelog.com

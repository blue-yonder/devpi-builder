=========
Changelog
=========

This lists the most important changes for each release.


v2.2.0 (May 05 2016)
====================

- Capture build errors for better output in case of build failures. Thanks Travis Mehlinger.


v2.1.0 (Apr 22 2016)
====================

- Add support for client certificates. Thanks Hans Lawrenz.


v2.0.0 (Jan 20 2016)
====================

- Enable compatibility with pip >= 8.0 by relying on pip's default download cache
  mechanism instead of explicitly requiring a download cache. This effectively
  disables caching for people still using pip < 6.0.
  Thanks Christian Stefanescu.
- Support for dry-running the wheel build without changing the devpi server state.
- Python 3.5 is now officially supported.
- Python 3.2 is no longer supported.


v1.0.0 (May 22 2015)
====================

- Use devpi-plumber_ instead of a custom devpi wrapper.
- Check the blacklist first when deciding whether to build a package.


v0.4.0 (Nov 13 2014)
====================

- Only consider a package to exist if it is a wheel and it is compatible with
  the current system. Thanks Michael Still and David Szotten
- Fix source distribution by adding missing README.md.
  Thanks Mikhail Lukyanchenko.


v0.3.0 (Aug 15 2014)
====================

- support for special-case handling of pure python wheels 
- optional support for report skipped packages in a JUnit-compatible XML
- Python 3 support


v0.2.1 (Aug 07 2014)
====================

- fix crash if a build wheel could cannot be found
  (because pip<=1.5.2 skipped it)


v0.2.0 (Aug 01 2014)
====================

- support for package blacklisting to never build certain wheels
- build as many packages as possible. Do not stop if one fails.


v0.1.0 (Aug 01 2014)
====================

- Initial release


.. _devpi-plumber: https://github.com/blue-yonder/devpi-plumber

Changelog
=========

v0.5.0
------

- Use [devpi-plumber](https://github.com/blue-yonder/devpi-plumber) instead of
  a custom devpi wrapper.

v0.4.0 (Nov 13 2014)
--------------------

- Only consider a package to exist if it is a wheel and it is compatible with
  the current system. Thanks Michael Still and David Szotten
- Fix source distribution by adding missing README.md.
  Thanks Mikhail Lukyanchenko


v0.3.0 (Aug 15 2014)
--------------------

- support for special-case handling of pure python wheels 
- optional support for report skipped packages in a JUnit-compatible XML
- Python 3 support


v0.2.1 (Aug 07 2014)
--------------------

- fix crash if a build wheel could cannot be found
  (because pip<=1.5.2 skipped it)


v0.2.0 (Aug 01 2014)
--------------------

- support for package blacklisting to never build certain wheels
- build as many packages as possible. Do not stop if one fails.


v0.1.0 (Aug 01 2014)
--------------------

- Initial release

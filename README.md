Brandon the Devpi Builder
=========================

This tools takes a list of python packages, specified as in an `requirements.txt` and incrementally fills a
[devpi](http://doc.devpi.net/latest/) index with them.

Features
--------

 * Reads a `requirements.txt` stile input file.
 * Multiple versions of a package may be imported.
 * Only builds packages not yet in the target index.
 * Can use separate indices for plain python packages and those with binary contents.
    - Optionally only operates on one of the two.


Planned
-------
 * Supports a black-list for packages to never be built and uploaded (certain packages like numpy are fragile regarding
   their interdependency with other packages).
 * Support extras

License
-------

New BSD

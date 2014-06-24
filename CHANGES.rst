Changelog
---------

Here you can see the full list of changes between each intervals release.


0.3.1 (2014-06-24)
^^^^^^^^^^^^^^^^^^

- Fixed setup.py packages


0.3.0 (2014-03-18)
^^^^^^^^^^^^^^^^^^

- Added __bool__ implementation for all interval types
- Added __int__ support for IntInterval


0.2.4 (2014-02-25)
^^^^^^^^^^^^^^^^^^

- Added step argument to AbstractInterval constructor

0.2.3 (2014-02-25)
^^^^^^^^^^^^^^^^^^

- Improved hyphen range parsing
- Fixed glb and lub methods
- Added inf and sup methods


0.2.2 (2014-02-20)
^^^^^^^^^^^^^^^^^^

- Fixed comparison to None
- Added glb and lub methods


0.2.1 (2014-02-17)
^^^^^^^^^^^^^^^^^^

- Fixed __lt__ and __le__ operators (total_ordering was not working)


0.2.0 (2014-01-10)
^^^^^^^^^^^^^^^^^^

- Added improved arithmetics
- Added centre, radius, discrete and length properties
- Added support for custom typed intervals
- Added support for discrete intervals
- Added support for __radd__ and __rsub__
- Added degenerate property
- Added support for contains
- Added Interval subclasses (IntInterval, DateInterval, DateTimeInterval, FloatInterval and DecimalInterval)
- Updated infinity dependency to 0.1.3


0.1.1 (2014-01-09)
^^^^^^^^^^^^^^^^^^

- Added interval length property


0.1.0 (2014-01-09)
^^^^^^^^^^^^^^^^^^

- Initial public release

Changelog
---------

Here you can see the full list of changes between each intervals release.


0.8.0 (2016-07-10)
^^^^^^^^^^^^^^^^^^

- Added is_connected utility method
- Made interval constructor throw IllegalArgument exception for intervals such as (a..a)
- Fixed some edge cases with interval intersections
- Fixed interval union (#33)


0.7.1 (2016-03-05)
^^^^^^^^^^^^^^^^^^

- Added support for step argument in ``from_string`` factory method
- Added better error message when passing string as a first constructor argument


0.7.0 (2016-02-27)
^^^^^^^^^^^^^^^^^^

- Added canonicalize to main module import
- Added factory methods for easier interval initialization ``open``, ``closed``, ``open_closed``, ``closed_open``, ``greater_than``, ``at_least``, ``less_than``, ``at_most`` and ``all``
- Renamed ``open`` and ``closed`` properties to ``is_open`` and ``is_closed``


0.6.0 (2016-01-28)
^^^^^^^^^^^^^^^^^^

- Removed interval constructor string parsing
- Added new class method from_string


0.5.0 (2014-03-25)
^^^^^^^^^^^^^^^^^^

- Drop python 2.6 support


0.4.0 (2014-10-30)
^^^^^^^^^^^^^^^^^^

- Made intervals hashable
- Added CharacterInterval class


0.3.2 (2014-10-21)
^^^^^^^^^^^^^^^^^^

- Fixed interval datetime type guessing
- Fixed code examples in docs
- Fixed IntInterval step rounding
- Added better test suite (now docs are tested also)


0.3.1 (2014-06-24)
^^^^^^^^^^^^^^^^^^

- Fixed setup.py packages


0.3.0 (2014-03-18)
^^^^^^^^^^^^^^^^^^

- Added ``__bool__`` implementation for all interval types
- Added ``__int__`` support for ``IntInterval``


0.2.4 (2014-02-25)
^^^^^^^^^^^^^^^^^^

- Added step argument to ``AbstractInterval`` constructor

0.2.3 (2014-02-25)
^^^^^^^^^^^^^^^^^^

- Improved hyphen range parsing
- Fixed ``glb`` and ``lub`` methods
- Added ``inf`` and ``sup`` methods


0.2.2 (2014-02-20)
^^^^^^^^^^^^^^^^^^

- Fixed comparison to ``None``
- Added ``glb`` and ``lub`` methods


0.2.1 (2014-02-17)
^^^^^^^^^^^^^^^^^^

- Fixed ``__lt__`` and ``__le__`` operators (``total_ordering`` was not working)


0.2.0 (2014-01-10)
^^^^^^^^^^^^^^^^^^

- Added improved arithmetics
- Added ``centre``, ``radius``, ``discrete`` and ``length`` properties
- Added support for custom typed intervals
- Added support for discrete intervals
- Added support for ``__radd__`` and ``__rsub__``
- Added ``degenerate`` property
- Added support for contains
- Added ``Interval`` subclasses (``IntInterval``, ``DateInterval``,
  ``DateTimeInterval``, ``FloatInterval`` and ``DecimalInterval``)
- Updated infinity dependency to 0.1.3


0.1.1 (2014-01-09)
^^^^^^^^^^^^^^^^^^

- Added interval ``length`` property


0.1.0 (2014-01-09)
^^^^^^^^^^^^^^^^^^

- Initial public release

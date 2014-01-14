intervals
=========

|Build Status| |Version Status| |Downloads|

Python tools for handling intervals (ranges of comparable objects).


Interval initialization
-----------------------


.. code-block:: python


    # All integers between 1 and 4
    interval = Interval([1, 4])

    interval.lower      # 1
    interval.upper      # 4

    interval.lower_inc  # True
    interval.upper_inc  # True


Open, half-open and closed intervals
------------------------------------

Intervals can be either open, half-open or closed. Properties `lower_inc` and `upper_inc` denote whether or not given endpoint is included (open) or not.

* An open interval is an interval where both endpoints are open.

.. code-block:: python

    interval = Interval((1, 4))

    interval.open           # True
    interval.lower_inc      # False
    interval.upper_inc      # False


* Half-open interval has one of the endpoints as open

.. code-block:: python

    interval = Interval('[1, 4)')

    interval.open           # False
    interval.lower_inc      # True
    interval.upper_inc      # False

* Closed interval includes both endpoints

.. code-block:: python

    interval = Interval([1, 4])

    interval.closed         # True
    interval.lower_inc      # True
    interval.upper_inc      # True



Interval types
--------------

Each interval encapsulates a type. Interval is not actually a class. Its a convenient factory that generates `AbstractInterval` subclasses. Whenever you call `Interval()` the IntervalFactory tries to guess to best matching interval for given bounds.



.. code-block:: python

    from datetime import date


    interval = Interval([1, 4])
    interval                        # IntInterval('[1, 4]')
    interval.type                   # int

    interval = Interval([1.5, 4])
    interval                        # FloatInterval('[1.5, 4]')
    interval.type                   # float

    interval = Interval([date(2000, 1, 1), inf])
    interval                        # DateInterval('[2000-1-1,)')
    interval.type                   # date


You can also create interval subtypes directly (this is also faster than using `Interval`).


.. code-block:: python

    IntInterval([1, 4])

    FloatInterval((1.4, 2.7))

Currently provided subtypes are:

* `IntInterval`
* `FloatInterval`
* `DecimalInterval`
* `DateInterval`
* `DateTimeInterval`


Properties
----------

* `radius` gives the half-length of an interval

.. code-block:: python

    Interval([1, 4]).radius             # 2.5

* `length` gives the length of an interval.

.. code-block:: python

    Interval([1, 4]).length             # 3

* `centre` gives the centre (midpoint) of an interval

.. code-block:: python

    Interval([-1, 1]).centre            # 0

* Interval [a, b] is `degenerate` if a == b

.. code-block:: python

    Interval([1, 1]).degenerate         # True
    Interval([1, 2]).degenerate         # False


Operators
---------

.. code-block:: python

    Interval([1, 5]) > Interval([0, 3])     # True

    Interval([1, 5]) == Interval([1, 5])    # True

    Interval([2, 3]) in Interval([2, 6])    # True

    Interval([2, 3]) in Interval([2, 3])    # True

    Interval([2, 3]) in Interval((2, 3))    # False


Discrete intervals
------------------


.. code-block:: python


    Interval([2, 4]) == Interval((1, 5))    # True


Arithmetics
-----------

.. code-block:: python


    Interval([1, 5]) + Interval([1, 8])     # Interval([2, 13])


    # intersection

    Interval([2, 6]) & Interval([3, 8])     # Interval([3, 6])


.. |Build Status| image:: https://travis-ci.org/kvesteri/intervals.png?branch=master
   :target: https://travis-ci.org/kvesteri/intervals
.. |Version Status| image:: https://pypip.in/v/intervals/badge.png
   :target: https://crate.io/packages/intervals/
.. |Downloads| image:: https://pypip.in/d/intervals/badge.png
   :target: https://crate.io/packages/intervals/

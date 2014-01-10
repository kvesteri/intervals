intervals
=========

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


Interval types
--------------

Each interval encapsulates a type. You can pass the type as a constructor parameter. If no type is given as a constructor parameter
intervals tries to guess the type of the interval.


.. code-block:: python

    from datetime import date


    Interval([1, 4]).type               # int

    Interval([1.5, 4]).type             # float

    Interval([date(2000, 1, 1), inf])   # date

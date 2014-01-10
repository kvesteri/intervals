intervals
=========

Python tools for handling intervals (ranges of comparable objects).


.. highlight:: python


::

    # All integers between 1 and 4
    interval = Interval([1, 4])

    interval.lower      # 1
    interval.upper      # 4

    interval.lower_inc  # True
    interval.upper_inc  # True



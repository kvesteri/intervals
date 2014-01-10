from datetime import date
from intervals import Interval, canonicalize


def test_canonicalize_integer_intervals():
    assert canonicalize(Interval([1, 4])).normalized == '[1, 5)'
    assert canonicalize(
        Interval((1, 7)), lower_inc=True, upper_inc=True
    ).normalized == '[2, 6]'
    assert canonicalize(
        Interval([1, 7]), lower_inc=False, upper_inc=True
    ).normalized == '(0, 7]'


def test_canonicalize_date_intervals():
    interval = canonicalize(Interval([date(2000, 2, 2), date(2000, 2, 6)]))
    assert interval.upper.day == 7

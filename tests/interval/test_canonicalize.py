from datetime import date

from intervals import canonicalize, DateInterval, IntInterval


def test_canonicalize_integer_intervals():
    assert str(canonicalize(IntInterval([1, 4]))) == '[1, 5)'
    assert str(canonicalize(
        IntInterval((1, 7)), lower_inc=True, upper_inc=True
    )) == '[2, 6]'
    assert str(canonicalize(
        IntInterval([1, 7]), lower_inc=False, upper_inc=True
    )) == '(0, 7]'


def test_canonicalize_date_intervals():
    interval = canonicalize(DateInterval([date(2000, 2, 2), date(2000, 2, 6)]))
    assert interval.upper.day == 7

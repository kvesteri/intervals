from intervals import Interval, canonicalize


def test_canonicalize():
    assert canonicalize(Interval([1, 4])).normalized == '[1, 5)'
    assert canonicalize(
        Interval((1, 7)), lower_inc=True, upper_inc=True
    ).normalized == '[2, 6]'
    assert canonicalize(
        Interval([1, 7]), lower_inc=False, upper_inc=True
    ).normalized == '(0, 7]'

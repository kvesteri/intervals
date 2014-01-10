from pytest import raises, mark
from intervals import Interval, RangeBoundsException
from infinity import inf


def test_str_representation():
    assert str(Interval((1, 3))) == '1 - 3'
    assert str(Interval((1, 1))) == '1'


def test_normalized_str():
    assert Interval((1, inf)).normalized == '(1,)'


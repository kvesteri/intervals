from pytest import mark

from intervals import IntInterval


@mark.parametrize(('interval', 'string'), (
    (IntInterval((1, 3)), '2'),
    (IntInterval([1, 1]), '1'),
    (IntInterval([1, 3]), '1 - 3'),
    (IntInterval.from_string('(1, 5]'), '2 - 5'),
    (IntInterval.from_string('[1,]'), '1 -')
))
def test_hyphenized(interval, string):
    assert interval.hyphenized == string

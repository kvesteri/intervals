from pytest import mark
from intervals import Interval
from infinity import inf


@mark.parametrize(('interval', 'string'), (
    ((1, 3), '(1, 3)'),
    ([1, 1], '[1, 1]'),
    ([1, inf], '[1,]')
))
def test_str_representation(interval, string):
    assert str(Interval(interval)) == string


@mark.parametrize(('interval', 'string'), (
    ((1, 3), '2'),
    ([1, 1], '1'),
    ([1, 3], '1 - 3'),
    ('(1, 5]', '2 - 5'),
    ('[1,]', '1 -')
))
def test_hyphenized(interval, string):
    assert Interval(interval).hyphenized == string


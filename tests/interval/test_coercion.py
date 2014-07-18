from pytest import mark, raises
from intervals import IntInterval
from infinity import inf


@mark.parametrize(('interval', 'string'), (
    ((1, 3), '(1, 3)'),
    ([1, 1], '[1, 1]'),
    ([1, inf], '[1,]')
))
def test_str_representation(interval, string):
    assert str(IntInterval(interval)) == string


@mark.parametrize(
    ('number_range', 'empty'),
    (
        ((2, 3), True),
        ([2, 3], False),
        ([2, 2], False),
        ((2, 2), True),
        ('[2, 2)', True),
        ('(2, 2]', True),
        ('[2, 3)', False),
        ((2, 10), False),
    )
)
def test_bool(number_range, empty):
    assert bool(IntInterval(number_range)) != empty


@mark.parametrize(
    ('number_range', 'coerced_value'),
    (
        ([5, 5], 5),
        ([2, 2], 2),
    )
)
def test_int_with_single_point_interval(number_range, coerced_value):
    assert int(IntInterval(number_range)) == coerced_value


@mark.parametrize(
    ('number_range'),
    (
        '[2, 2)',
        '(2, 2]',
    )
)
def test_int_with_empty_interval(number_range):
    with raises(TypeError):
        int(IntInterval(number_range))


@mark.parametrize(
    ('number_range'),
    (
        [2, 4],
        [2, 5],
    )
)
def test_int_with_interval_containing_multiple_points(number_range):
    with raises(TypeError):
        int(IntInterval(number_range))

from pytest import raises, mark
from intervals import (
    Interval, IntervalException, RangeBoundsException
)
from infinity import inf


class TestIntervalInit(object):
    def test_support_range_object(self):
        interval = Interval(Interval(1, 3))
        assert interval.lower == 1
        assert interval.upper == 3
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_multiple_args(self):
        interval = Interval(1, 3)
        assert interval.lower == 1
        assert interval.upper == 3
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_strings(self):
        interval = Interval('1-3')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_infinity(self):
        interval = Interval(-inf, inf)
        assert interval.lower == -inf
        assert interval.upper == inf
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_strings_with_spaces(self):
        interval = Interval('1 - 3')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_strings_with_bounds(self):
        interval = Interval('[1, 3]')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_empty_string_as_upper_bound(self):
        interval = Interval('[1,)')
        assert interval.lower == 1
        assert interval.upper == inf
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_empty_string_as_lower_bound(self):
        interval = Interval('[,1)')
        assert interval.lower == -inf
        assert interval.upper == 1
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_supports_exact_ranges_as_strings(self):
        interval = Interval('3')
        assert interval.lower == 3
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_integers(self):
        interval = Interval(3)
        assert interval.lower == 3
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc


def test_str_representation():
    assert str(Interval(1, 3)) == '1 - 3'
    assert str(Interval(1, 1)) == '1'


def test_normalized_str():
    assert Interval(1, inf).normalized == '(1,)'


@mark.parametrize('number_range',
    (
        (3, 2),
        [4, 2],
        '5-2',
        (float('inf'), 2),
        '[4, 3]',
    )
)
def test_raises_exception_for_badly_constructed_range(number_range):
    with raises(RangeBoundsException):
        Interval(number_range)


@mark.parametrize(('number_range', 'is_open'),
    (
        ((2, 3), True),
        ('(2, 5)', True),
        ('[3, 4)', False),
        ('(4, 5]', False),
        ('3 - 4', False),
        ([4, 5], False),
        ('[4, 5]', False)
    )
)
def test_open(number_range, is_open):
    assert Interval(number_range).open == is_open


@mark.parametrize(('number_range', 'is_closed'),
    (
        ((2, 3), False),
        ('(2, 5)', False),
        ('[3, 4)', False),
        ('(4, 5]', False),
        ('3 - 4', True),
        ([4, 5], True),
        ('[4, 5]', True)
    )
)
def test_closed(number_range, is_closed):
    assert Interval(number_range).closed == is_closed

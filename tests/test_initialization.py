from pytest import raises, mark
from intervals import Interval, RangeBoundsException
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

    @mark.parametrize('number_range',
        (
            (3, 2),
            [4, 2],
            '5-2',
            (float('inf'), 2),
            '[4, 3]',
        )
    )
    def test_raises_exception_for_badly_constructed_range(self, number_range):
        with raises(RangeBoundsException):
            Interval(number_range)

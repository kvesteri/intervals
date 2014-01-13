from decimal import Decimal
from pytest import raises, mark
from intervals import (
    DecimalInterval,
    FloatInterval,
    Interval,
    IntInterval,
    RangeBoundsException
)
from infinity import inf


class TestIntervalInit(object):
    def test_floats(self):
        interval = FloatInterval((0.2, 0.5))
        assert interval.lower == 0.2
        assert interval.upper == 0.5
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_decimals(self):
        interval = DecimalInterval((Decimal('0.2'), Decimal('0.5')))
        assert interval.lower == Decimal('0.2')
        assert interval.upper == Decimal('0.5')
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_support_range_object(self):
        interval = IntInterval(IntInterval((1, 3)))
        assert interval.lower == 1
        assert interval.upper == 3
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_strings(self):
        interval = IntInterval('1-3')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_infinity(self):
        interval = IntInterval((-inf, inf))
        assert interval.lower == -inf
        assert interval.upper == inf
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_strings_with_spaces(self):
        interval = IntInterval('1 - 3')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_strings_with_bounds(self):
        interval = IntInterval('[1, 3]')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_empty_string_as_upper_bound(self):
        interval = IntInterval('[1,)')
        assert interval.lower == 1
        assert interval.upper == inf
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_empty_string_as_lower_bound(self):
        interval = IntInterval('[,1)')
        assert interval.lower == -inf
        assert interval.upper == 1
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_supports_exact_ranges_as_strings(self):
        interval = IntInterval('3')
        assert interval.lower == 3
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_integers(self):
        interval = IntInterval(3)
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
            IntInterval(number_range)


class TestTypeGuessing(object):
    @mark.parametrize(('number_range', 'type'),
        (
            ((2, 3), int),
            ([-6, 8], int),
            (8.5, float),
            ([Decimal(2), 9], int),
            ([Decimal('0.5'), 9], float),
        )
    )
    def test_guesses_types(self, number_range, type):
        assert Interval(number_range).type == type

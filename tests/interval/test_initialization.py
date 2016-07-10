from datetime import date
from decimal import Decimal

from infinity import inf
from pytest import mark, raises

from intervals import (
    CharacterInterval,
    DecimalInterval,
    FloatInterval,
    IllegalArgument,
    Interval,
    IntInterval,
    RangeBoundsException
)


class TestIntervalInit(object):
    def test_string_as_constructor_param(self):
        with raises(TypeError) as e:
            FloatInterval('(0.2, 0.5)')
        assert (
            'First argument should be a list or tuple. If you wish to '
            'initialize an interval from string, use from_string factory '
            'method.'
        ) in str(e)

    def test_invalid_argument(self):
        with raises(IllegalArgument) as e:
            FloatInterval((0, 0))
        assert (
            'The bounds may be equal only if at least one of the bounds is '
            'closed.'
        ) in str(e)

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
        interval = IntInterval.from_string('1-3')
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
        interval = IntInterval.from_string('1 - 3')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_strings_with_bounds(self):
        interval = IntInterval.from_string('[1, 3]')
        assert interval.lower == 1
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_step_argument_for_from_string(self):
        interval = IntInterval.from_string('[2,)', step=2)
        assert interval.lower == 2
        assert interval.upper == inf
        assert interval.step == 2

    def test_empty_string_as_upper_bound(self):
        interval = IntInterval.from_string('[1,)')
        assert interval.lower == 1
        assert interval.upper == inf
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_empty_string_as_lower_bound(self):
        interval = IntInterval.from_string('[,1)')
        assert interval.lower == -inf
        assert interval.upper == 1
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_supports_exact_ranges_as_strings(self):
        interval = IntInterval.from_string('3')
        assert interval.lower == 3
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_integers(self):
        interval = IntInterval(3)
        assert interval.lower.__class__ == int
        assert interval.lower == 3
        assert interval.upper == 3
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_character_intervals(self):
        interval = CharacterInterval(('a', 'z'))
        assert interval.lower == 'a'
        assert interval.upper == 'z'
        assert not interval.lower_inc
        assert not interval.upper_inc

    def test_supports_characters_from_strings(self):
        interval = CharacterInterval.from_string('A-Z')
        assert interval.lower == 'A'
        assert interval.upper == 'Z'
        assert interval.lower_inc
        assert interval.upper_inc

    def test_supports_characters_with_spaces(self):
        interval = CharacterInterval.from_string('A - Z')
        assert interval.lower == 'A'
        assert interval.upper == 'Z'
        assert interval.lower_inc
        assert interval.upper_inc

    def test_empty_string_as_upper_character_bound(self):
        interval = CharacterInterval.from_string('[a,)')
        assert interval.lower == 'a'
        assert interval.upper == inf
        assert interval.lower_inc
        assert not interval.upper_inc

    def test_empty_string_as_lower_bound_for_char_interval(self):
        interval = CharacterInterval.from_string('[,a)')
        assert interval.lower == -inf
        assert interval.upper == 'a'
        assert interval.lower_inc
        assert not interval.upper_inc

    @mark.parametrize(
        ('number_range', 'lower', 'upper'),
        (
            ('-2-2', -2, 2),
            ('-3--2', -3, -2),
            ('2-3', 2, 3),
            ('2-', 2, inf),
            ('-5', -5, -5)
        )
    )
    def test_hyphen_format(self, number_range, lower, upper):
        interval = IntInterval.from_string(number_range)
        assert interval.lower == lower
        assert interval.upper == upper

    @mark.parametrize(
        ('constructor', 'number_range'),
        (
            (IntInterval, (3, 2)),
            (IntInterval, [4, 2]),
            (IntInterval, (float('inf'), 2)),
            (CharacterInterval, ('c', 'b')),
            (CharacterInterval, ('d', 'b')),
            (CharacterInterval, (inf, 'b')),
        )
    )
    def test_raises_exception_for_badly_constructed_range(
        self,
        constructor,
        number_range
    ):
        with raises(RangeBoundsException):
            constructor(number_range)


class TestTypeGuessing(object):
    @mark.parametrize(
        ('number_range', 'type'),
        (
            ((2, 3), int),
            ([-6, 8], int),
            (8.5, float),
            ([Decimal(2), 9], int),
            ([Decimal('0.5'), 9], float),
            ([date(2000, 1, 1), inf], date),
            (('a', 'e'), str),
        )
    )
    def test_guesses_types(self, number_range, type):
        assert Interval(number_range).type == type

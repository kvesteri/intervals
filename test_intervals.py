from pytest import raises, mark
from intervals import (
    Interval, IntervalException, RangeBoundsException
)


class TestIntervalInit(object):
    def test_support_range_object(self):
        num_range = Interval(Interval(1, 3))
        assert num_range.lower == 1
        assert num_range.upper == 3

    def test_supports_multiple_args(self):
        num_range = Interval(1, 3)
        assert num_range.lower == 1
        assert num_range.upper == 3

    def test_supports_strings(self):
        num_range = Interval('1-3')
        assert num_range.lower == 1
        assert num_range.upper == 3

    def test_supports_strings_with_spaces(self):
        num_range = Interval('1 - 3')
        assert num_range.lower == 1
        assert num_range.upper == 3

    def test_supports_strings_with_bounds(self):
        num_range = Interval('[1, 3]')
        assert num_range.lower == 1
        assert num_range.upper == 3

    def test_empty_string_as_upper_bound(self):
        num_range = Interval('[1,)')
        assert num_range.lower == 1
        assert num_range.upper == float('inf')

    def test_supports_exact_ranges_as_strings(self):
        num_range = Interval('3')
        assert num_range.lower == 3
        assert num_range.upper == 3

    def test_supports_integers(self):
        num_range = Interval(3)
        assert num_range.lower == 3
        assert num_range.upper == 3


class TestComparisonOperators(object):
    def test_eq_operator(self):
        assert Interval(1, 3) == Interval(1, 3)
        assert not Interval(1, 3) == Interval(1, 4)

    def test_ne_operator(self):
        assert not Interval(1, 3) != Interval(1, 3)
        assert Interval(1, 3) != Interval(1, 4)

    def test_gt_operator(self):
        assert Interval(1, 3) > Interval(0, 2)
        assert not Interval(2, 3) > Interval(2, 3)

    def test_ge_operator(self):
        assert Interval(1, 3) >= Interval(0, 2)
        assert Interval(1, 3) >= Interval(1, 3)

    def test_lt_operator(self):
        assert Interval(0, 2) < Interval(1, 3)
        assert not Interval(2, 3) < Interval(2, 3)

    def test_le_operator(self):
        assert Interval(0, 2) <= Interval(1, 3)
        assert Interval(1, 3) >= Interval(1, 3)

    def test_integer_comparison(self):
        assert Interval(2, 2) <= 3
        assert Interval(1, 3) >= 0
        assert Interval(2, 2) == 2
        assert Interval(2, 2) != 3


def test_str_representation():
    assert str(Interval(1, 3)) == '1 - 3'
    assert str(Interval(1, 1)) == '1'



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


class TestArithmeticOperators(object):
    def test_add_operator(self):
        assert Interval(1, 2) + Interval(1, 2) == Interval(2, 4)

    def test_sub_operator(self):
        assert Interval(1, 3) - Interval(1, 2) == Interval(-1, 2)

    def test_isub_operator(self):
        range_ = Interval(1, 3)
        range_ -= Interval(1, 2)
        assert range_ == Interval(-1, 2)

    def test_iadd_operator(self):
        range_ = Interval(1, 2)
        range_ += Interval(1, 2)
        assert range_ == Interval(2, 4)

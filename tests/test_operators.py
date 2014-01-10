from pytest import mark
from intervals import Interval


class TestComparisonOperators(object):
    def test_eq_operator(self):
        assert Interval([1, 3]) == Interval([1, 3])
        assert not Interval([1, 3]) == Interval([1, 4])

    def test_ne_operator(self):
        assert not Interval([1, 3]) != Interval([1, 3])
        assert Interval([1, 3]) != Interval([1, 4])

    def test_gt_operator(self):
        assert Interval([1, 3]) > Interval([0, 2])
        assert not Interval([2, 3]) > Interval([2, 3])

    @mark.parametrize(('comparison', 'result'), (
        (Interval([1, 3]) >= Interval([0, 2]), True),
        (Interval((1, 4)) >= 1, False),
        (Interval((1, 6)) >= [1, 6], False),
        (Interval((1, 6)) >= 0, True)
    ))
    def test_ge_operator(self, comparison, result):
        assert comparison == result

    def test_lt_operator(self):
        assert Interval([0, 2]) < Interval([1, 3])
        assert not Interval([2, 3]) < Interval([2, 3])

    def test_le_operator(self):
        assert Interval([0, 2]) <= Interval([1, 3])
        assert Interval([1, 3]) >= Interval([1, 3])

    def test_integer_comparison(self):
        assert Interval([2, 2]) <= 3
        assert Interval([1, 3]) >= 0
        assert Interval([2, 2]) == 2
        assert Interval([2, 2]) != 3

    @mark.parametrize('value', (
        Interval([0, 2]),
        1,
        (-1, 1),
    ))
    def test_contains_operator_for_inclusive_interval(self, value):
        assert value in Interval([-1, 2])

    @mark.parametrize('value', (
        Interval([0, 2]),
        2,
        '[-1, 1]',
    ))
    def test_contains_operator_for_non_inclusive_interval(self, value):
        assert value not in Interval((-1, 2))


class TestDiscreteRangeComparison(object):
    @mark.parametrize(('interval', 'interval2'), (
        ([1, 3], '[1, 4)'),
        ('(1, 5]', '[2, 5]'),
        ('(1, 6)', '[2, 5]'),
    ))
    def test_eq_operator(self, interval, interval2):
        assert Interval(interval) == Interval(interval2)

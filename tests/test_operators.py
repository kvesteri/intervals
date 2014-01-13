from pytest import mark
from intervals import IntInterval


class TestComparisonOperators(object):
    def test_eq_operator(self):
        assert IntInterval([1, 3]) == IntInterval([1, 3])
        assert not IntInterval([1, 3]) == IntInterval([1, 4])

    def test_ne_operator(self):
        assert not IntInterval([1, 3]) != IntInterval([1, 3])
        assert IntInterval([1, 3]) != IntInterval([1, 4])

    def test_gt_operator(self):
        assert IntInterval([1, 3]) > IntInterval([0, 2])
        assert not IntInterval([2, 3]) > IntInterval([2, 3])

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([1, 3]) >= IntInterval([0, 2]), True),
        (IntInterval((1, 4)) >= 1, False),
        (IntInterval((1, 6)) >= [1, 6], False),
        (IntInterval((1, 6)) >= 0, True)
    ))
    def test_ge_operator(self, comparison, result):
        assert comparison == result

    def test_lt_operator(self):
        assert IntInterval([0, 2]) < IntInterval([1, 3])
        assert not IntInterval([2, 3]) < IntInterval([2, 3])

    def test_le_operator(self):
        assert IntInterval([0, 2]) <= IntInterval([1, 3])
        assert IntInterval([1, 3]) >= IntInterval([1, 3])

    def test_integer_comparison(self):
        assert IntInterval([2, 2]) <= 3
        assert IntInterval([1, 3]) >= 0
        assert IntInterval([2, 2]) == 2
        assert IntInterval([2, 2]) != 3

    @mark.parametrize('value', (
        IntInterval([0, 2]),
        1,
        (-1, 1),
    ))
    def test_contains_operator_for_inclusive_interval(self, value):
        assert value in IntInterval([-1, 2])

    @mark.parametrize('value', (
        IntInterval([0, 2]),
        2,
        '[-1, 1]',
    ))
    def test_contains_operator_for_non_inclusive_interval(self, value):
        assert value not in IntInterval((-1, 2))


class TestDiscreteRangeComparison(object):
    @mark.parametrize(('interval', 'interval2'), (
        ([1, 3], '[1, 4)'),
        ('(1, 5]', '[2, 5]'),
        ('(1, 6)', '[2, 5]'),
    ))
    def test_eq_operator(self, interval, interval2):
        assert IntInterval(interval) == IntInterval(interval2)

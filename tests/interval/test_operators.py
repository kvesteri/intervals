from datetime import date

from infinity import inf
from pytest import mark, raises

from intervals import DateInterval, FloatInterval, IllegalArgument, IntInterval


class TestComparisonOperators(object):
    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([1, 3]) == IntInterval([1, 3]), True),
        (IntInterval([1, 3]) == IntInterval([1, 4]), False),
        (IntInterval([inf, inf]) == inf, True),
        (IntInterval([3, 3]) == 3, True),
        (IntInterval([3, 3]) == 5, False),
        (IntInterval([3, 3]) == 'something', False),
        (
            IntInterval([3, 3]) ==
            DateInterval([date(2011, 1, 1), date(2011, 1, 1)]),
            False
        ),
        (IntInterval.from_string('(,)') == None, False)  # noqa
    ))
    def test_eq_operator(self, comparison, result):
        assert comparison is result

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([1, 3]) != IntInterval([1, 3]), False),
        (IntInterval([1, 3]) != IntInterval([1, 4]), True),
        (IntInterval([inf, inf]) != inf, False),
        (IntInterval([3, 3]) != 3, False),
        (IntInterval([3, 3]) != 5, True),
        (IntInterval([3, 3]) != 'something', True),
        (IntInterval.from_string('(,)') != None, True)  # noqa
    ))
    def test_ne_operator(self, comparison, result):
        assert comparison is result

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([1, 3]) > IntInterval([0, 2]), True),
        (IntInterval((1, 4)) > 1, False),
        (IntInterval((1, 6)) > [1, 6], False),
        (IntInterval((1, 6)) > 0, True)
    ))
    def test_gt_operator(self, comparison, result):
        assert comparison is result

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([1, 3]) >= IntInterval([0, 2]), True),
        (IntInterval((1, 4)) >= 1, False),
        (IntInterval((1, 6)) >= [1, 6], False),
        (IntInterval((1, 6)) >= 0, True)
    ))
    def test_ge_operator(self, comparison, result):
        assert comparison is result

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([0, 2]) < IntInterval([1, 3]), True),
        (IntInterval([2, 3]) < IntInterval([2, 3]), False),
        (IntInterval([2, 5]) < 6, True),
        (IntInterval([2, 5]) < 5, False),
        (IntInterval([2, 5]) < inf, True)
    ))
    def test_lt_operator(self, comparison, result):
        assert comparison is result

    @mark.parametrize(('comparison', 'result'), (
        (IntInterval([0, 2]) <= IntInterval([1, 3]), True),
        (IntInterval([1, 3]) <= IntInterval([1, 3]), True),
        (IntInterval([1, 7]) <= 8, True),
        (IntInterval([1, 6]) <= 5, False),
        (IntInterval([1, 5]) <= inf, True)
    ))
    def test_le_operator(self, comparison, result):
        assert comparison is result

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
        [-1, 1],
    ))
    def test_contains_operator_for_non_inclusive_interval(self, value):
        assert value not in IntInterval((-1, 2))

    @mark.parametrize(('interval1', 'interval2', 'expected'), (
        (IntInterval((0, 2)), IntInterval((0, 2)), True),
        (IntInterval([0, 2]), IntInterval([0, 2]), True),
        (
            IntInterval.from_string('[0, 2)'),
            IntInterval.from_string('[0, 2)'),
            True
        ),
        (
            IntInterval.from_string('(0, 2]'),
            IntInterval.from_string('(0, 2]'),
            True
        ),
        (IntInterval((0, 2)), IntInterval((1, 2)), False),
        (IntInterval((0, 2)), IntInterval((0, 1)), False),
        (IntInterval((0, 2)), IntInterval([0, 1]), False),
        (IntInterval((0, 2)), FloatInterval((0, 1)), False),
    ))
    def test_hash_operator_with_interval_attributes(
        self,
        interval1,
        interval2,
        expected
    ):
        actual = (interval1.__hash__() == interval2.__hash__())
        assert actual == expected

    @mark.parametrize(('contains_check', 'expected'), (
        (IntInterval([0, 2]) in {IntInterval([0, 2]): ''}, True),
        (IntInterval([0, 2]) in {IntInterval((0, 2)): ''}, False),
        (IntInterval([0, 2]) in set([IntInterval([0, 2])]), True),
    ))
    def test_hash_operator_with_collections(self, contains_check, expected):
        assert contains_check is expected


class TestDiscreteRangeComparison(object):
    @mark.parametrize(('interval', 'interval2'), (
        ('[1, 3]', '[1, 4)'),
        ('(1, 5]', '[2, 5]'),
        ('(1, 6)', '[2, 5]'),
    ))
    def test_eq_operator(self, interval, interval2):
        assert (
            IntInterval.from_string(interval) ==
            IntInterval.from_string(interval2)
        )


class TestBinaryOperators(object):
    @mark.parametrize(('interval1', 'interval2', 'result'), (
        ('(2, 3]', '[3, 4)', IntInterval([3, 3])),
        ('(2, 10]', '[3, 40]', IntInterval([3, 10])),
        ('[0, 0]', '[0, 0]', IntInterval.from_string('[0, 0]')),
        ('[0, 0]', '(0, 0]', IntInterval.from_string('(0, 0]')),
        ('[0, 0)', '[0, 0]', IntInterval.from_string('[0, 0)')),
        ('(2, 2]', '(2, 2]', IntInterval.from_string('(2, 2]')),
        ('[2, 2)', '[2, 2)', IntInterval.from_string('[2, 2)')),
        ('(2, 3)', '[3, 4]', IntInterval.from_string('[3, 3)')),
        ('[2, 3]', '(3, 4)', IntInterval.from_string('(3, 3]')),
    ))
    def test_and_operator(
        self,
        interval1,
        interval2,
        result
    ):
        assert (
            IntInterval.from_string(interval1) &
            IntInterval.from_string(interval2) ==
            result
        )

    @mark.parametrize(('interval1', 'interval2'), (
        ('[2, 2]', '[5, 7)'),
        ('(2, 3]', '[4, 40]'),
        ('(2, 3)', '(3, 4)'),
    ))
    def test_and_operator_with_illegal_arguments(self, interval1, interval2):
        with raises(IllegalArgument):
            (
                IntInterval.from_string(interval1) &
                IntInterval.from_string(interval2)
            )

    @mark.parametrize(('interval1', 'interval2'), (
        ('[2, 2]', '[5, 7)'),
        ('(2, 3]', '[4, 40]'),
        ('(2, 3)', '(3, 4)'),
    ))
    def test_or_operator_with_illegal_arguments(self, interval1, interval2):
        with raises(IllegalArgument):
            (
                IntInterval.from_string(interval1) |
                IntInterval.from_string(interval2)
            )

    @mark.parametrize(('interval1', 'interval2', 'result'), (
        ('(2, 3]', '[3, 4)', IntInterval.from_string('(2, 4)')),
        ('(2, 10]', '[3, 40]', IntInterval.from_string('(2, 40]')),
        ('[0, 0]', '[0, 0]', IntInterval.from_string('[0, 0]')),
        ('[0, 0]', '(0, 0]', IntInterval.from_string('[0, 0]')),
        ('[0, 0)', '[0, 0]', IntInterval.from_string('[0, 0]')),
        ('(2, 2]', '(2, 2]', IntInterval.from_string('(2, 2]')),
        ('[2, 2)', '[2, 2)', IntInterval.from_string('[2, 2)')),
        ('(2, 3)', '[3, 4]', IntInterval.from_string('(2, 4]')),
        ('[2, 3]', '(3, 4)', IntInterval.from_string('[2, 4)')),
    ))
    def test_or_operator(
        self,
        interval1,
        interval2,
        result
    ):
        assert (
            IntInterval.from_string(interval1) |
            IntInterval.from_string(interval2) ==
            result
        )

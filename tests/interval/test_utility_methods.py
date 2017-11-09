from pytest import mark

from intervals import DecimalInterval, IntInterval


@mark.parametrize(
    ('interval1', 'interval2', 'result'),
    (
        (IntInterval([1, 3]), IntInterval([1, 3]), True),
        (
            DecimalInterval.from_string('[1, 3)'),
            DecimalInterval.from_string('[3, 4]'),
            True
        ),
        (
            DecimalInterval.from_string('[3, 4]'),
            DecimalInterval.from_string('[1, 3)'),
            True
        ),
        (
            DecimalInterval.from_string('[1, 3]'),
            DecimalInterval.from_string('[4, 5]'),
            False
        ),
        (
            DecimalInterval.from_string('[2, 4)'),
            DecimalInterval.from_string('[0, 1]'),
            False
        ),
        (
            DecimalInterval.from_string('[1, 3)'),
            DecimalInterval.from_string('(3, 4]'),
            False
        ),
        (
            IntInterval([1, 2]),
            IntInterval([3, 4]),
            True
        ),
    )
)
def test_is_connected(interval1, interval2, result):
    assert interval1.is_connected(interval2) is result


# TODO: test with non-discrete intervals
@mark.parametrize(
    'interval_1, interval_2, result',
    [
        (
            IntInterval([1, 4]),
            IntInterval([7, 10]),
            IntInterval((4, 7)),
        ), (
            IntInterval([1, 4]),
            IntInterval([5, 6]),
            IntInterval((4, 5)),
        ), (
            IntInterval([1, 4]),
            IntInterval.from_string('(4, 6]'),
            IntInterval.from_string('(4, 4]'),
        ), (
            IntInterval.from_string('[1, 4)'),
            IntInterval.from_string('(4, 6]'),
            IntInterval([4, 4]),
        ), (
            IntInterval.from_string('[1, 1)'),
            IntInterval.from_string('(3, 3]'),
            IntInterval([1, 3]),
        ), (
            IntInterval.from_string('[1, 1)'),
            IntInterval.from_string('[3, 3)'),
            IntInterval.from_string('[1, 3)'),
        ), (
            IntInterval.from_string('(1, 1]'),
            IntInterval.from_string('(3, 3]'),
            IntInterval.from_string('(1, 3]'),
        ), (
            IntInterval([1, 4]),
            IntInterval([2, 6]),
            None,
        ), (
            IntInterval([1, 4]),
            IntInterval([1, 4]),
            None,
        ), (
            DecimalInterval([1, 3]),
            DecimalInterval([4, 5]),
            DecimalInterval((3, 4)),
        ), (
            DecimalInterval((1, 3)),
            DecimalInterval([3, 5]),
            DecimalInterval.from_string('[3, 3)'),
        ),
    ])
def test_gap_interval(interval_1, interval_2, result):
    assert interval_1.gap_interval(interval_2) == result
    assert interval_2.gap_interval(interval_1) == result

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
        )
    )
)
def test_is_connected(interval1, interval2, result):
    assert interval1.is_connected(interval2) is result

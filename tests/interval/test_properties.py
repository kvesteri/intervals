from datetime import date, datetime
from decimal import Decimal

from infinity import inf
from pytest import mark

from intervals import (
    DateInterval,
    DateTimeInterval,
    DecimalInterval,
    FloatInterval,
    IntInterval
)


class TestIntervalProperties(object):
    @mark.parametrize(
        ('number_range', 'length'),
        (
            ([1, 4], 3),
            ([-1, 1], 2),
            ((-inf, inf), inf),
            ((1, inf), inf),
        )
    )
    def test_length(self, number_range, length):
        assert IntInterval(number_range).length == length

    @mark.parametrize(
        ('number_range', 'radius'),
        (
            ([1, 4], 1.5),
            ([-1, 1], 1.0),
            ([-4, -1], 1.5),
            ((-inf, inf), inf),
            ((1, inf), inf),
        )
    )
    def test_radius(self, number_range, radius):
        assert IntInterval(number_range).radius == radius

    @mark.parametrize(
        ('number_range', 'centre'),
        (
            ([1, 4], 2.5),
            ([-1, 1], 0),
            ([-4, -1], -2.5),
            ((1, inf), inf),
        )
    )
    def test_centre(self, number_range, centre):
        assert IntInterval(number_range).centre == centre

    @mark.parametrize(
        ('interval', 'is_open'),
        (
            (IntInterval((2, 3)), True),
            (IntInterval.from_string('(2, 5)'), True),
            (IntInterval.from_string('[3, 4)'), False),
            (IntInterval.from_string('(4, 5]'), False),
            (IntInterval.from_string('3 - 4'), False),
            (IntInterval([4, 5]), False),
            (IntInterval.from_string('[4, 5]'), False)
        )
    )
    def test_is_open(self, interval, is_open):
        assert interval.is_open == is_open

    @mark.parametrize(
        ('interval', 'is_closed'),
        (
            (IntInterval((2, 3)), False),
            (IntInterval.from_string('(2, 5)'), False),
            (IntInterval.from_string('[3, 4)'), False),
            (IntInterval.from_string('(4, 5]'), False),
            (IntInterval.from_string('3 - 4'), True),
            (IntInterval([4, 5]), True),
            (IntInterval.from_string('[4, 5]'), True)
        )
    )
    def test_closed(self, interval, is_closed):
        assert interval.is_closed == is_closed

    @mark.parametrize(
        ('interval', 'empty'),
        (
            (IntInterval((2, 3)), True),
            (IntInterval([2, 3]), False),
            (IntInterval([2, 2]), False),
            (IntInterval.from_string('[2, 2)'), True),
            (IntInterval.from_string('(2, 2]'), True),
            (IntInterval.from_string('[2, 3)'), False),
            (IntInterval((2, 10)), False),
        )
    )
    def test_empty(self, interval, empty):
        assert interval.empty == empty

    @mark.parametrize(
        ('interval', 'degenerate'),
        (
            (IntInterval((2, 4)), False),
            (IntInterval.from_string('[2, 2]'), True),
            (IntInterval.from_string('[0, 0)'), True),
        )
    )
    def test_degenerate(self, interval, degenerate):
        assert interval.degenerate == degenerate

    @mark.parametrize(
        ('interval', 'discrete'),
        (
            (IntInterval((2, 3)), True),
            (IntInterval(5), True),
            (FloatInterval(3.5), False),
            (DecimalInterval(Decimal('2.4')), False),
            (DateTimeInterval(datetime(2002, 1, 1)), False),
            (DateInterval(date(2002, 1, 1)), True)
        )
    )
    def test_discrete(self, interval, discrete):
        assert interval.discrete == discrete

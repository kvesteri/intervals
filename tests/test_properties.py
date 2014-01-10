from datetime import datetime, date
from decimal import Decimal
from pytest import mark
from intervals import Interval
from infinity import inf


class TestIntervalProperties(object):
    @mark.parametrize(('number_range', 'length'),
        (
            ([1, 4], 3),
            ([-1, 1], 2),
            ((-inf, inf), inf),
            ((1, inf), inf),
        )
    )
    def test_length(self, number_range, length):
        assert Interval(number_range).length == length

    @mark.parametrize(('number_range', 'radius'),
        (
            ([1, 4], 1.5),
            ([-1, 1], 1.0),
            ([-4, -1], 1.5),
            ((-inf, inf), inf),
            ((1, inf), inf),
        )
    )
    def test_radius(self, number_range, radius):
        assert Interval(number_range).radius == radius

    @mark.parametrize(('number_range', 'centre'),
        (
            ([1, 4], 2.5),
            ([-1, 1], 0),
            ([-4, -1], -2.5),
            ((1, inf), inf),
        )
    )
    def test_centre(self, number_range, centre):
        assert Interval(number_range).centre == centre

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
    def test_open(self, number_range, is_open):
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
    def test_closed(self, number_range, is_closed):
        assert Interval(number_range).closed == is_closed

    @mark.parametrize(('obj_range', 'discrete'),
        (
            ((2, 3), True),
            (5, True),
            (3.5, False),
            (Decimal('2.4'), False),
            (datetime(2002, 1, 1), False),
            (date(2002, 1, 1), True)
        )
    )
    def test_discrete(self, obj_range, discrete):
        assert Interval(obj_range).discrete == discrete

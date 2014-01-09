from pytest import mark
from intervals import Interval
from infinity import inf


class TestIntervalProperties(object):
    def test_length(self):
        assert Interval([1, 4]).length == 3
        assert Interval([-1, 1]).length == 2
        assert Interval(-inf, inf).length == inf
        assert Interval(1, inf).length == inf

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

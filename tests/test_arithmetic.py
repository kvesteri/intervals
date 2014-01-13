from pytest import mark
from intervals import IntInterval


class TestArithmeticOperators(object):
    @mark.parametrize(('first', 'second', 'result'), (
        (IntInterval([1, 3]), IntInterval([1, 2]), [2, 5]),
        (IntInterval([1, 3]), 1, [2, 4]),
        (1, IntInterval([1, 3]), [2, 4]),
        ([1, 2], IntInterval([1, 2]), [2, 4])
    ))
    def test_add_operator(self, first, second, result):
        assert first + second == IntInterval(result)

    @mark.parametrize(('first', 'second', 'result'), (
        (IntInterval([1, 3]), IntInterval([1, 2]), [-1, 2]),
        (IntInterval([1, 3]), 1, [0, 2]),
        (1, IntInterval([1, 3]), [-2, 0])
    ))
    def test_sub_operator(self, first, second, result):
        assert first - second == IntInterval(result)

    def test_isub_operator(self):
        range_ = IntInterval([1, 3])
        range_ -= IntInterval([1, 2])
        assert range_ == IntInterval([-1, 2])

    def test_iadd_operator(self):
        range_ = IntInterval([1, 2])
        range_ += IntInterval([1, 2])
        assert range_ == IntInterval([2, 4])

    @mark.parametrize(('first', 'second', 'intersection'), (
        ('[1, 5]', '[2, 9]', '[2, 5]'),
        ('[3, 4]', '[3, 9]', '[3, 4]'),
        ('(3, 6]', '[2, 6)', '(3, 6)')
    ))
    def test_intersection(self, first, second, intersection):
        IntInterval(first) & IntInterval(second) == IntInterval(intersection)

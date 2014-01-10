from pytest import mark
from intervals import Interval


class TestArithmeticOperators(object):
    def test_add_operator(self):
        assert Interval([1, 2]) + Interval([1, 2]) == Interval([2, 4])

    @mark.parametrize(('first', 'second', 'result'), (
        (Interval([1, 3]), Interval([1, 2]), [-1, 2]),
        (Interval([1, 3]), 1, [0, 2]),
        (1, Interval([1, 3]), [-2, 0])
    ))
    def test_sub_operator(self, first, second, result):
        assert first - second == Interval(result)

    def test_isub_operator(self):
        range_ = Interval([1, 3])
        range_ -= Interval([1, 2])
        assert range_ == Interval([-1, 2])

    def test_iadd_operator(self):
        range_ = Interval([1, 2])
        range_ += Interval([1, 2])
        assert range_ == Interval([2, 4])

    @mark.parametrize(('first', 'second', 'intersection'), (
        ('[1, 5]', '[2, 9]', '[2, 5]'),
        ('[3, 4]', '[3, 9]', '[3, 4]'),
        ('(3, 6]', '[2, 6)', '(3, 6)')
    ))
    def test_intersection(self, first, second, intersection):
        Interval(first) & Interval(second) == Interval(intersection)

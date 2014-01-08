from intervals import Interval


class TestArithmeticOperators(object):
    def test_add_operator(self):
        assert Interval(1, 2) + Interval(1, 2) == Interval(2, 4)

    def test_sub_operator(self):
        assert Interval(1, 3) - Interval(1, 2) == Interval(-1, 2)

    def test_isub_operator(self):
        range_ = Interval(1, 3)
        range_ -= Interval(1, 2)
        assert range_ == Interval(-1, 2)

    def test_iadd_operator(self):
        range_ = Interval(1, 2)
        range_ += Interval(1, 2)
        assert range_ == Interval(2, 4)

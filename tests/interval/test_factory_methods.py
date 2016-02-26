from infinity import inf

from intervals import IntInterval


class TestFactoryMethods(object):
    def test_open(self):
        interval = IntInterval.open(12, 14, step=2)
        assert interval.lower == 12
        assert interval.upper == 14
        assert interval.is_open
        assert interval.step == 2

    def test_closed(self):
        interval = IntInterval.closed(10, 11, step=2)
        assert interval.lower == 10
        assert interval.upper == 12
        assert interval.is_closed
        assert interval.step == 2

    def test_open_closed(self):
        interval = IntInterval.open_closed(10, 14, step=2)
        assert interval.lower == 10
        assert interval.upper == 14
        assert not interval.lower_inc
        assert interval.upper_inc
        assert interval.step == 2

    def test_closed_open(self):
        interval = IntInterval.closed_open(10, 14, step=2)
        assert interval.lower == 10
        assert interval.upper == 14
        assert interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == 2

    def test_greater_than(self):
        interval = IntInterval.greater_than(10, step=2)
        assert interval.lower == 10
        assert interval.upper == inf
        assert not interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == 2

    def test_at_least(self):
        interval = IntInterval.at_least(10, step=2)
        assert interval.lower == 10
        assert interval.upper == inf
        assert interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == 2

    def test_less_than(self):
        interval = IntInterval.less_than(10, step=2)
        assert interval.lower == -inf
        assert interval.upper == 10
        assert not interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == 2

    def test_at_most(self):
        interval = IntInterval.at_most(10, step=2)
        assert interval.lower == -inf
        assert interval.upper == 10
        assert not interval.lower_inc
        assert interval.upper_inc
        assert interval.step == 2

    def test_all(self):
        interval = IntInterval.all(step=2)
        assert interval.lower == -inf
        assert interval.upper == inf
        assert not interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == 2

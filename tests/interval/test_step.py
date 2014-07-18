from decimal import Decimal
from intervals import (
    DecimalInterval,
    FloatInterval,
    Interval,
    IntInterval,
    RangeBoundsException
)


class TestStepWithFloats(object):
    def test_decimals_with_step(self):
        interval = FloatInterval((0, 0.5), step=0.5)
        assert interval.lower == 0
        assert interval.upper == 0.5
        assert not interval.lower_inc
        assert not interval.upper_inc
        assert interval.step

    def test_step_rounding(self):
        interval = FloatInterval((0.2, 0.8), step=0.5)
        assert interval.lower == 0
        assert interval.upper == 1


class TestStepWithDecimals(object):
    def test_decimals_with_step(self):
        interval = DecimalInterval(
            (Decimal('0'), Decimal('0.5')),
            step=Decimal('0.5')
        )
        assert interval.lower == 0
        assert interval.upper == Decimal('0.5')
        assert not interval.lower_inc
        assert not interval.upper_inc
        assert interval.step == Decimal('0.5')

    def test_step_rounding(self):
        interval = DecimalInterval(
            (Decimal('0.2'), Decimal('0.8')),
            step=Decimal('0.5')
        )
        assert interval.lower == 0
        assert interval.upper == 1

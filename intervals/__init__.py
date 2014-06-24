"""
http://grouper.ieee.org/groups/1788/PositionPapers/ARITHYY.pdf

http://grouper.ieee.org/groups/1788/PositionPapers/overlapping.pdf

www.wikipedia.org/Interval
"""

# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from decimal import Decimal
import operator
try:
    from functools import total_ordering
except ImportError:
    from total_ordering import total_ordering
from infinity import inf, is_infinite
import six
from .parser import IntervalParser
from .exc import IntervalException, RangeBoundsException


__all__ = (
    RangeBoundsException
)


__version__ = '0.3.1'


def is_number(number):
    return isinstance(number, (float, int, Decimal))


def canonicalize_lower(interval, inc=True):
    if not interval.lower_inc and inc:
        return interval.lower + interval.step, True
    elif not inc and interval.lower_inc:
        return interval.lower - interval.step, False
    else:
        return interval.lower, interval.lower_inc


def canonicalize_upper(interval, inc=False):
    if not interval.upper_inc and inc:
        return interval.upper - interval.step, True
    elif not inc and interval.upper_inc:
        return interval.upper + interval.step, False
    else:
        return interval.upper, interval.upper_inc


def canonicalize(interval, lower_inc=True, upper_inc=False):
    """
    Canonicalize converts equivalent discrete intervals to different
    representations.
    """
    if not interval.discrete:
        raise TypeError('Only discrete ranges can be canonicalized')

    if interval.empty:
        return interval

    lower, lower_inc = canonicalize_lower(interval, lower_inc)
    upper, upper_inc = canonicalize_upper(interval, upper_inc)

    return interval.__class__(
        [lower, upper],
        lower_inc=lower_inc,
        upper_inc=upper_inc,
    )


def coerce_interval(func):
    def wrapper(self, arg):
        try:
            if arg is not None:
                arg = self.__class__(arg)
            return func(self, arg)
        except IntervalException:
            return NotImplemented
    return wrapper


class AbstractInterval(object):
    step = None
    type = None
    parser = IntervalParser()

    def __init__(
        self,
        bounds,
        lower_inc=None,
        upper_inc=None,
        step=None
    ):
        """
        Parses given args and assigns lower and upper bound for this number
        range.

        1. Comma separated string argument

        ::


            >>> range = IntInterval('[23, 45]')
            >>> range.lower
            23
            >>> range.upper
            45


            >>> range = IntInterval('(23, 45]')
            >>> range.lower_inc
            False

            >>> range = IntInterval('(23, 45)')
            >>> range.lower_inc
            False
            >>> range.upper_inc
            False

        2. Lists and tuples as an argument

        ::


            >>> range = IntInterval([23, 45])
            >>> range.lower
            23
            >>> range.upper
            45
            >>> range.closed
            True


            >>> range = IntInterval((23, 45))
            >>> range.lower
            23
            >>> range.closed
            False

        3. Integer argument

        ::


            >>> range = IntInterval(34)
            >>> range.lower == range.upper == 34
            True


        4. Object argument

        ::

            >>> range = IntInterval(IntInterval(20, 30))
            >>> range.lower
            20
            >>> range.upper
            30

        """
        if step is not None:
            self.step = step
        self.lower, self.upper, self.lower_inc, self.upper_inc = (
            self.parser(bounds, lower_inc, upper_inc)
        )

        if self.lower > self.upper:
            raise RangeBoundsException(
                self.lower,
                self.upper
            )

    def copy_args(self, interval):
        self.lower_inc = interval.lower_inc
        self.upper_inc = interval.upper_inc
        self.lower = interval.lower
        self.upper = interval.upper
        self.type = interval.type

    def coerce_value(self, value):
        if value is None or value == '':
            return None
        elif is_infinite(value):
            return value
        elif isinstance(value, six.string_types):
            return self.coerce_string(value)
        else:
            return self.coerce_obj(value)

    def coerce_string(self, value):
        return self.type(value)

    def coerce_obj(self, obj):
        return obj

    @property
    def lower(self):
        return self._lower

    @lower.setter
    def lower(self, value):
        value = self.coerce_value(value)
        if value is None:
            self._lower = -inf
        else:
            self._lower = self.round_value_by_step(value)

    @property
    def upper(self):
        return self._upper

    @upper.setter
    def upper(self, value):
        value = self.coerce_value(value)
        if value is None:
            self._upper = inf
        else:
            self._upper = self.round_value_by_step(value)

    def round_value_by_step(self, value):
        return value

    @property
    def open(self):
        """
        Returns whether or not this object is an open interval.

        ::

            range = Interval('(23, 45)')
            range.open  # True

            range = Interval('[23, 45]')
            range.open  # False
        """
        return not self.lower_inc and not self.upper_inc

    @property
    def closed(self):
        """
        Returns whether or not this object is a closed interval.

        ::

            range = Interval('(23, 45)')
            range.closed  # False

            range = Interval('[23, 45]')
            range.closed  # True
        """
        return self.lower_inc and self.upper_inc

    def __str__(self):
        return '%s%s,%s%s' % (
            '[' if self.lower_inc else '(',
            str(self.lower) if not is_infinite(self.lower) else '',
            ' ' + str(self.upper) if not is_infinite(self.upper) else '',
            ']' if self.upper_inc else ')'
        )

    def equals(self, other):
        return (
            self.lower == other.lower and
            self.upper == other.upper and
            self.lower_inc == other.lower_inc and
            self.upper_inc == other.upper_inc and
            self.type == other.type
        )

    @coerce_interval
    def __eq__(self, other):
        try:
            if self.discrete:
                return canonicalize(self).equals(canonicalize(other))
            return self.equals(other)
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    @coerce_interval
    def __gt__(self, other):
        return self.lower > other.lower and self.upper > other.upper

    @coerce_interval
    def __lt__(self, other):
        return self.lower < other.lower and self.upper < other.upper

    @coerce_interval
    def __ge__(self, other):
        return self == other or self > other

    @coerce_interval
    def __le__(self, other):
        return self == other or self < other

    @coerce_interval
    def __contains__(self, other):
        lower_op = (
            operator.le
            if self.lower_inc or (not self.lower_inc and not other.lower_inc)
            else operator.lt
        )

        upper_op = (
            operator.ge
            if self.upper_inc or (not self.upper_inc and not other.upper_inc)
            else operator.gt
        )
        return (
            lower_op(self.lower, other.lower) and
            upper_op(self.upper, other.upper)
        )

    @property
    def discrete(self):
        """
        Returns whether or not this interval is discrete.
        """
        return self.step is not None

    @property
    def length(self):
        return abs(self.upper - self.lower)

    @property
    def radius(self):
        if self.length == inf:
            return inf
        return float(self.length) / 2

    @property
    def degenerate(self):
        return self.upper == self.lower

    @property
    def empty(self):
        if self.discrete and not self.degenerate:
            return (
                self.upper - self.lower == self.step
                and not (self.upper_inc or self.lower_inc)
            )
        return (
            self.upper == self.lower
            and not (self.lower_inc and self.upper_inc)
        )

    def __bool__(self):
        return not self.empty

    def __nonzero__(self):
        return not self.empty

    @property
    def centre(self):
        return float((self.lower + self.upper)) / 2

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    @property
    def hyphenized(self):
        if not self.discrete:
            raise TypeError('Only discrete intervals have hyphenized format.')
        c = canonicalize(self, True, True)

        if c.lower != c.upper:
            return '%s -%s' % (
                str(c.lower) if not is_infinite(c.lower) else '',
                ' ' + str(c.upper) if not is_infinite(c.upper) else ''
            )
        return str(c.lower)

    @coerce_interval
    def __add__(self, other):
        """
        [a, b] + [c, d] = [a + c, b + d]
        """
        return self.__class__(
            [
                self.lower + other.lower,
                self.upper + other.upper
            ],
            lower_inc=self.lower_inc if self < other else other.lower_inc,
            upper_inc=self.upper_inc if self > other else other.upper_inc,
        )

    __radd__ = __add__

    @coerce_interval
    def __sub__(self, other):
        """
        Defines the substraction operator.

        [a, b] - [c, d] = [a - d, b - c]
        """
        return self.__class__([
            self.lower - other.upper,
            self.upper - other.lower
        ])

    @coerce_interval
    def glb(self, other):
        """
        Return the greatest lower bound for given intervals.

        :param other: AbstractInterval instance
        """
        return self.__class__(
            [
                min(self.lower, other.lower),
                min(self.upper, other.upper)
            ],
            lower_inc=self.lower_inc if self < other else other.lower_inc,
            upper_inc=self.upper_inc if self > other else other.upper_inc,
        )

    @coerce_interval
    def lub(self, other):
        """
        Return the least upper bound for given intervals.

        :param other: AbstractInterval instance
        """
        return self.__class__(
            [
                max(self.lower, other.lower),
                max(self.upper, other.upper),
            ],
            lower_inc=self.lower_inc if self < other else other.lower_inc,
            upper_inc=self.upper_inc if self > other else other.upper_inc,
        )

    @coerce_interval
    def inf(self, other):
        """
        Return the infimum of given intervals.

        :param other: AbstractInterval instance
        """
        return self.__class__(
            [
                max(self.lower, other.lower),
                min(self.upper, other.upper),
            ],
            lower_inc=self.lower_inc if self < other else other.lower_inc,
            upper_inc=self.upper_inc if self > other else other.upper_inc,
        )

    @coerce_interval
    def sup(self, other):
        """
        Return the supremum of given intervals.

        :param other: AbstractInterval instance
        """
        return self.__class__(
            [
                min(self.lower, other.lower),
                max(self.upper, other.upper),
            ],
            lower_inc=self.lower_inc if self < other else other.lower_inc,
            upper_inc=self.upper_inc if self > other else other.upper_inc,
        )

    @coerce_interval
    def __rsub__(self, other):
        return self.__class__([
            other.lower - self.upper,
            other.upper - self.lower
        ])

    def __and__(self, other):
        """
        Defines the intersection operator
        """
        if self.upper < other.lower or other.upper < self.lower:
            return self.__class__((0, 0))
        if self.lower <= other.lower <= self.upper:
            intersection = self.__class__([
                other.lower,
                other.upper if other.upper < self.upper else self.upper
            ])
            intersection.lower_inc = other.lower_inc
            intersection.upper_inc = (
                other.upper_inc if other.upper < self.upper else self.upper_inc
            )
        elif self.lower <= other.upper <= self.upper:
            intersection = self.__class__([
                other.lower if other.lower > self.lower else self.lower,
                other.upper
            ])
            intersection.lower_inc = (
                other.lower_inc if other.lower > self.lower else self.lower_inc
            )
            intersection.upper_inc = other.upper_inc
        else:
            return other & self
        return intersection

    def __or__(self, other):
        """
        Defines the union operator
        """
        if self.upper < other.lower or other.upper < self.lower:
            raise IntervalException(
                'Union is not continuous.'
            )
        return self.sup(other)


class NumberInterval(AbstractInterval):
    def round_value_by_step(self, value):
        if self.step and not is_infinite(value):
            return self.type(
                self.step *
                round((self.type(Decimal('1.0')) / self.step) * value)
            )
        return value


class IntInterval(NumberInterval):
    step = 1
    type = int

    def coerce_obj(self, obj):
        if isinstance(obj, float) or isinstance(obj, Decimal):
            if str(int(obj)) != str(obj):
                raise IntervalException(
                    'Could not coerce %s to int. Decimal places would '
                    'be lost.'
                )
            return int(obj)
        return obj

    def __int__(self):
        if self.empty:
            raise TypeError('Empty intervals cannot be coerced to integers')
        if self.lower != self.upper:
            raise TypeError(
                'Only intervals containing single point can be coerced to'
                ' integers'
            )
        return self.lower


class DateInterval(AbstractInterval):
    step = timedelta(days=1)
    type = date


class DateTimeInterval(NumberInterval):
    type = datetime


class FloatInterval(NumberInterval):
    type = float


class DecimalInterval(NumberInterval):
    type = Decimal

    def round_value_by_step(self, value):
        if self.step and not is_infinite(value):
            return self.type(str(
                float(self.step) *
                round(1.0 / float(self.step) * float(value))
            ))
        return value


class IntervalFactory(object):
    interval_classes = [
        IntInterval,
        FloatInterval,
        DecimalInterval,
        DateInterval,
        DateTimeInterval
    ]

    def __call__(self, bounds, lower_inc=None, upper_inc=None, step=None):
        for interval_class in self.interval_classes:
            try:
                return interval_class(
                    bounds,
                    lower_inc=lower_inc,
                    upper_inc=upper_inc,
                    step=step
                )
            except IntervalException:
                pass
        raise IntervalException(
            'Could not initialize interval.'
        )

Interval = IntervalFactory()

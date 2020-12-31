"""
http://grouper.ieee.org/groups/1788/PositionPapers/ARITHYY.pdf

http://grouper.ieee.org/groups/1788/PositionPapers/overlapping.pdf

https://en.wikipedia.org/wiki/Interval_(mathematics)
"""

# -*- coding: utf-8 -*-
import operator
from datetime import date, datetime, timedelta
from decimal import Decimal
from math import ceil, floor

from infinity import inf, is_infinite

from .exc import IllegalArgument, IntervalException, RangeBoundsException
from .parser import IntervalParser, IntervalStringParser

try:
    string_types = basestring,  # Python 2
except NameError:
    string_types = str,  # Python 3


def is_number(number):
    return isinstance(number, (float, int, Decimal))


def py2round(value):
    """Round values as in Python 2, for Python 3 compatibility.

    All x.5 values are rounded away from zero.

    In Python 3, this has changed to avoid bias: when x is even,
    rounding is towards zero, when x is odd, rounding is away
    from zero. Thus, in Python 3, round(2.5) results in 2,
    round(3.5) is 4.

    Python 3 also returns an int; Python 2 returns a float.
    """
    if value > 0:
        return float(floor(float(value)+0.5))
    else:
        return float(ceil(float(value)-0.5))


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
    Convert equivalent discrete intervals to different representations.
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
        if (
            isinstance(arg, list) or
            isinstance(arg, tuple) or
            isinstance(arg, self.type) or
            isinstance(arg, type(self)) or
            arg == inf or arg == -inf
        ):
            try:
                if arg is not None:
                    arg = type(self)(arg)
                return func(self, arg)
            except IntervalException:
                return NotImplemented
        try:
            arg = type(self)(self.type(arg))
        except (ValueError, TypeError, OverflowError):
            pass
        return func(self, arg)
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
        Parse given args and assign lower and upper bound for this number
        range.

        1. Comma separated string argument::

            >>> range = IntInterval.from_string('[23, 45]')
            >>> range.lower
            23
            >>> range.upper
            45

            >>> range = IntInterval.from_string('(23, 45]')
            >>> range.lower_inc
            False

            >>> range = IntInterval.from_string('(23, 45)')
            >>> range.lower_inc
            False
            >>> range.upper_inc
            False

        2. Lists and tuples as an argument::

            >>> range = IntInterval([23, 45])
            >>> range.lower
            23
            >>> range.upper
            45
            >>> range.is_closed
            True

            >>> range = IntInterval((23, 45))
            >>> range.lower
            23
            >>> range.is_closed
            False

        3. Integer argument::

            >>> range = IntInterval(34)
            >>> range.lower == range.upper == 34
            True

        4. Object argument::

            >>> range = IntInterval(IntInterval((20, 30)))
            >>> range.lower
            20
            >>> range.upper
            30

        """
        if isinstance(bounds, string_types):
            raise TypeError(
                'First argument should be a list or tuple. If you wish to '
                'initialize an interval from string, use from_string factory '
                'method.'
            )

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
        if (
            self.lower == self.upper and
            not self.lower_inc and
            not self.upper_inc
        ):
            raise IllegalArgument(
                'The bounds may be equal only if at least one of the bounds '
                'is closed.'
            )

    @classmethod
    def open(cls, lower_bound, upper_bound, **kwargs):
        return cls(
            [lower_bound, upper_bound],
            lower_inc=False,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def closed(cls, lower_bound, upper_bound, **kwargs):
        return cls(
            [lower_bound, upper_bound],
            lower_inc=True,
            upper_inc=True,
            **kwargs
        )

    @classmethod
    def open_closed(cls, lower_bound, upper_bound, **kwargs):
        return cls(
            [lower_bound, upper_bound],
            lower_inc=False,
            upper_inc=True,
            **kwargs
        )

    @classmethod
    def closed_open(cls, lower_bound, upper_bound, **kwargs):
        return cls(
            [lower_bound, upper_bound],
            lower_inc=True,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def greater_than(cls, lower_bound, **kwargs):
        return cls(
            [lower_bound, inf],
            lower_inc=False,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def at_least(cls, lower_bound, **kwargs):
        return cls(
            [lower_bound, inf],
            lower_inc=True,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def less_than(cls, upper_bound, **kwargs):
        return cls(
            [-inf, upper_bound],
            lower_inc=False,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def at_most(cls, upper_bound, **kwargs):
        return cls(
            [-inf, upper_bound],
            lower_inc=False,
            upper_inc=True,
            **kwargs
        )

    @classmethod
    def all(cls, **kwargs):
        return cls(
            [-inf, inf],
            lower_inc=False,
            upper_inc=False,
            **kwargs
        )

    @classmethod
    def from_string(cls, bounds_string, **kwargs):
        return cls(
            *IntervalStringParser().parse_string(bounds_string),
            **kwargs
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
        elif isinstance(value, self.type):
            return value
        elif isinstance(value, string_types):
            return self.coerce_string(value)
        else:
            return self.coerce_obj(value)

    def coerce_string(self, value):
        return self.type(value)

    def coerce_obj(self, obj):
        return self.type(obj)

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
    def is_open(self):
        """
        Return whether or not this object is an open interval.

        Examples::

            >>> range = Interval.from_string('(23, 45)')
            >>> range.is_open
            True

            >>> range = Interval.from_string('[23, 45]')
            >>> range.is_open
            False

        """
        return not self.lower_inc and not self.upper_inc

    @property
    def is_closed(self):
        """
        Return whether or not this object is a closed interval.

        Examples::

            >>> range = Interval.from_string('(23, 45)')
            >>> range.is_closed
            False

            >>> range = Interval.from_string('[23, 45]')
            >>> range.is_closed
            True

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

    def __hash__(self):
        return (
            self.upper,
            self.lower,
            self.upper_inc,
            self.lower_inc,
            self.type
        ).__hash__()

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
        Return whether or not this interval is discrete.
        """
        return self.step is not None

    @property
    def length(self):
        if self.discrete:
            if not self:
                return 0
            if not self.lower_inc or not self.upper_inc:
                return canonicalize(self, lower_inc=True, upper_inc=True).length
        return abs(self.upper - self.lower)

    @property
    def radius(self):
        if self.length == inf:
            return inf
        return float(self.length) / 2

    @property
    def degenerate(self):
        """
        An interval is considered degenerate if it only contains one item or
        if it is empty.
        """
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
        Define the substraction operator.

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
        Return the infimum of given intervals. This is the same as
        intersection.

        :param other: AbstractInterval instance
        """
        return self & other

    @coerce_interval
    def sup(self, other):
        """
        Return the supremum of given intervals. This is the same as union.

        :param other: AbstractInterval instance
        """
        return self | other

    @coerce_interval
    def __rsub__(self, other):
        return self.__class__([
            other.lower - self.upper,
            other.upper - self.lower
        ])

    def __and__(self, other):
        """
        Define the intersection operator
        """
        if not self.is_connected(other):
            raise IllegalArgument(
                'Intersection is only supported for connected intervals.'
            )

        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)

        if self.lower < other.lower:
            lower_inc = other.lower_inc
        elif self.lower > other.lower:
            lower_inc = self.lower_inc
        else:
            lower_inc = self.lower_inc and other.lower_inc

        if self.upper > other.upper:
            upper_inc = other.upper_inc
        elif self.upper < other.upper:
            upper_inc = self.upper_inc
        else:
            upper_inc = self.upper_inc and other.upper_inc

        return self.__class__(
            [lower, upper],
            lower_inc=lower_inc,
            upper_inc=upper_inc
        )

    def __or__(self, other):
        """
        Define the union operator
        """
        if not self.is_connected(other):
            raise IllegalArgument('Union is not continuous.')
        lower = min(self.lower, other.lower)
        upper = max(self.upper, other.upper)

        if self.lower < other.lower:
            lower_inc = self.lower_inc
        elif self.lower > other.lower:
            lower_inc = other.lower_inc
        else:
            lower_inc = self.lower_inc or other.lower_inc

        if self.upper > other.upper:
            upper_inc = self.upper_inc
        elif self.upper < other.upper:
            upper_inc = other.upper_inc
        else:
            upper_inc = self.upper_inc or other.upper_inc

        return self.__class__(
            [lower, upper],
            lower_inc=lower_inc,
            upper_inc=upper_inc
        )

    def is_connected(self, other):
        """
        Returns ``True`` if there exists a (possibly empty) range which is
        enclosed by both this range and other.

        Examples:

        * [1, 3] and [5, 7] are not connected
        * [5, 7] and [1, 3] are not connected
        * [2, 4) and [3, 5) are connected, because both enclose [3, 4)
        * [1, 3) and [3, 5) are connected, because both enclose the empty range
          [3, 3)
        * [1, 3) and (3, 5) are not connected
        """
        return self.upper > other.lower and other.upper > self.lower or (
            self.upper == other.lower and (self.upper_inc or other.lower_inc)
        ) or (
            self.lower == other.upper and (self.lower_inc or other.upper_inc)
        )


class NumberInterval(AbstractInterval):
    rounding_type = Decimal

    def round_value_by_step(self, value):
        if self.step and not is_infinite(value):
            return self.type(
                self.rounding_type(self.step) *
                self.rounding_type(
                    py2round(
                        self.rounding_type('1.0') /
                        self.rounding_type(self.step) *
                        self.rounding_type(value)
                    )
                )
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


class DateTimeInterval(AbstractInterval):
    type = datetime


class FloatInterval(NumberInterval):
    type = float
    rounding_type = float


class DecimalInterval(NumberInterval):
    type = Decimal

    def round_value_by_step(self, value):
        if self.step and not is_infinite(value):
            return self.type(str(
                float(self.step) *
                py2round(1.0 / float(self.step) * float(value))
            ))
        return value


class CharacterInterval(AbstractInterval):
    type = str

    def coerce_obj(self, obj):
        if not isinstance(obj, str):
            raise IntervalException('Type %s is not a string.')
        return obj


class IntervalFactory(object):
    interval_classes = [
        CharacterInterval,
        IntInterval,
        FloatInterval,
        DecimalInterval,
        DateTimeInterval,
        DateInterval,
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
            except (IntervalException, TypeError):
                pass
        raise IntervalException(
            'Could not initialize interval.'
        )

    @classmethod
    def from_string(self, value):
        for interval_class in self.interval_classes:
            try:
                return interval_class.from_string(value)
            except (IntervalException, TypeError):
                pass
        raise IntervalException(
            'Could not initialize interval.'
        )

Interval = IntervalFactory()

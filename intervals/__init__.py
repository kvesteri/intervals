# -*- coding: utf-8 -*-
from collections import Iterable
from datetime import datetime, date, timedelta
from decimal import Decimal
try:
    from functools import total_ordering
except ImportError:
    from total_ordering import total_ordering
from infinity import inf, is_infinite, Infinity
import six


__version__ = '0.1.1'


class IntervalException(Exception):
    pass


class RangeBoundsException(IntervalException):
    def __init__(self, min_value, max_value):
        self.message = 'Min value %s is bigger than max value %s.' % (
            min_value,
            max_value
        )


def is_number(number):
    return isinstance(number, (float, int, Decimal))


def parse_number(number):
    if number is None or number == '':
        return None
    elif is_number(number):
        return number
    elif is_infinite(number):
        return number
    else:
        return int(number)


def canonicalized_bounds(interval, lower_inc=True, upper_inc=False):
    if not interval.discrete:
        raise TypeError('Only discrete ranges can be canonicalized')

    if not interval.lower_inc and lower_inc:
        lower = interval.lower + interval.step
    elif not lower_inc and interval.lower_inc:
        lower = interval.lower - interval.step
    else:
        lower = interval.lower

    if not interval.upper_inc and upper_inc:
        upper = interval.upper - interval.step
    elif not upper_inc and interval.upper_inc:
        upper = interval.upper + interval.step
    else:
        upper = interval.upper
    return lower, upper


def canonicalize(interval, lower_inc=True, upper_inc=False):
    """
    Canonicalize converts equivalent discrete intervals to different
    representations.
    """
    lower, upper = canonicalized_bounds(interval, lower_inc, upper_inc)

    return Interval(
        [lower, upper],
        lower_inc=lower_inc,
        upper_inc=upper_inc,
        type=interval.type,
        step=interval.step
    )


def coerce_interval(func):
    def wrapper(self, arg):
        try:
            return func(self, Interval(arg))
        except IntervalException:
            return NotImplemented
    return wrapper


@total_ordering
class Interval(object):
    def __init__(
        self,
        bounds,
        lower_inc=None,
        upper_inc=None,
        type=None,
        step=None,
        canonicalizer=canonicalize
    ):
        """
        Parses given args and assigns lower and upper bound for this number
        range.

        1. Comma separated string argument

        ::


            >>> range = Interval('[23, 45]')
            >>> range.lower
            23
            >>> range.upper
            45


            >>> range = Interval('(23, 45]')
            >>> range.lower_inc
            False

            >>> range = Interval('(23, 45)')
            >>> range.lower_inc
            False
            >>> range.upper_inc
            False

        2. Sequence of arguments

        ::


            >>> range = Interval(23, 45)
            >>> range.lower
            23
            >>> range.upper
            45


        3. Lists and tuples as an argument

        ::


            >>> range = Interval([23, 45])
            >>> range.lower
            23
            >>> range.upper
            45
            >>> range.closed
            True


            >>> range = Interval((23, 45))
            >>> range.lower
            23
            >>> range.closed
            False

        4. Integer argument

        ::


            >>> range = Interval(34)
            >>> range.lower == range.upper == 34
            True


        5. Object argument

        ::

            >>> range = Interval(Interval(20, 30))
            >>> range.lower
            20
            >>> range.upper
            30

        """
        if isinstance(bounds, six.string_types):
            self.parse_string(bounds)
        elif isinstance(bounds, Iterable):
            self.parse_sequence(bounds)
        elif hasattr(bounds, 'lower') and hasattr(bounds, 'upper'):
            self.parse_object(bounds)
        else:
            self.parse_single_value(bounds)

        if upper_inc is not None:
            self.upper_inc = upper_inc
        if lower_inc is not None:
            self.lower_inc = lower_inc

        self.type = (
            self._guess_type(self.lower, self.upper) if type is None else type
        )
        self.step = (
            self._guess_step(self.type) if step is None else step
        )

        if self.lower > self.upper:
            raise RangeBoundsException(self.lower, self.upper)

    def _guess_type(self, value, value2):
        def compare_type(value):
            types = [
                datetime,
                date,
                Decimal,
                float,
                int,
                Infinity
            ]
            return types.index(value.__class__)

        return min(value, value2, key=compare_type).__class__

    def _guess_step(self, type):
        steps = {
            int: 1,
            date: timedelta(days=1),
        }
        return steps.get(type, None)

    def copy_args(self, interval):
        self.lower_inc = interval.lower_inc
        self.upper_inc = interval.upper_inc
        self.lower = interval.lower
        self.upper = interval.upper
        self.type = interval.type
        self.canonicalizer = interval.canonicalizer

    @property
    def lower(self):
        return self._lower

    @lower.setter
    def lower(self, value):
        if value is None:
            self._lower = -inf
        else:
            self._lower = value

    @property
    def upper(self):
        return self._upper

    @upper.setter
    def upper(self, value):
        if value is None:
            self._upper = inf
        else:
            self._upper = value

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

    def parse_object(self, obj):
        self.lower = obj.lower
        self.upper = obj.upper
        self.lower_inc = obj.lower_inc
        self.upper_inc = obj.upper_inc

    def parse_string(self, value):
        if ',' not in value:
            self.parse_hyphen_range(value)
        else:
            self.parse_bounded_range(value)

    def parse_sequence(self, seq):
        lower, upper = seq
        self.lower = parse_number(lower)
        self.upper = parse_number(upper)
        if isinstance(seq, tuple):
            self.lower_inc = self.upper_inc = False
        else:
            self.lower_inc = self.upper_inc = True

    def parse_single_value(self, value):
        self.lower = self.upper = value
        self.lower_inc = self.upper_inc = True

    def parse_bounded_range(self, value):
        values = value.strip()[1:-1].split(',')
        try:
            lower, upper = map(
                lambda a: parse_number(a.strip()), values
            )
        except ValueError as e:
            raise IntervalException(e.message)

        self.lower_inc = value[0] == '['
        self.upper_inc = value[-1] == ']'
        self.lower = lower
        self.upper = upper

    def parse_hyphen_range(self, value):
        values = value.split('-')
        if len(values) == 1:
            self.lower = self.upper = parse_number(value.strip())
        else:
            try:
                self.lower, self.upper = map(
                    lambda a: parse_number(a.strip()), values
                )
            except ValueError as e:
                raise IntervalException(str(e))
        self.lower_inc = self.upper_inc = True

    @property
    def normalized(self):
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

    def __eq__(self, other):
        if isinstance(other, six.integer_types):
            return self.lower == other == self.upper
        try:
            if self.discrete:
                return canonicalize(self).equals(canonicalize(other))
            return self.equals(other)
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        if isinstance(other, six.integer_types):
            return self.lower > other and self.upper > other
        try:
            return self.lower > other.lower and self.upper > other.upper
        except AttributeError:
            return NotImplemented

    @property
    def discrete(self):
        """
        Returns whether or not this interval is discrete.
        """
        return (self.type in six.integer_types) or self.type == date

    @property
    def length(self):
        return abs(self.upper - self.lower)

    @property
    def radius(self):
        if self.length == inf:
            return inf
        return float(self.length) / 2

    @property
    def centre(self):
        return float((self.lower + self.upper)) / 2

    def __repr__(self):
        return "Interval(%r)" % self.normalized

    def __str__(self):
        if self.lower != self.upper:
            return '%s - %s' % (self.lower, self.upper)
        return str(self.lower)

    @coerce_interval
    def __add__(self, other):
        """
        [a, b] + [c, d] = [a + c, b + d]
        """
        try:
            return Interval([
                    self.lower + other.lower,
                    self.upper + other.upper
                ],
                lower_inc=self.lower_inc if self < other else other.lower_inc,
                upper_inc=self.upper_inc if self > other else other.upper_inc,
            )
        except AttributeError:
            return NotImplemented

    @coerce_interval
    def __sub__(self, other):
        """
        Defines the substraction operator.

        As defined in wikipedia:

        [a, b] − [c, d] = [a − d, b − c]
        """
        return Interval([
            self.lower - other.upper,
            self.upper - other.lower
        ])

    @coerce_interval
    def __rsub__(self, other):
        return Interval([
            other.lower - self.upper,
            other.upper - self.lower
        ])

    def __and__(self, other):
        """
        Defines the intersection operator
        """
        if self.lower <= other.lower <= self.upper:
            return Interval([
                other.lower,
                other.upper if other.upper < self.upper else self.upper
            ])
        elif self.lower <= other.upper <= self.upper:
            return Interval([
                other.lower if other.lower > self.lower else self.lower,
                other.upper
            ])

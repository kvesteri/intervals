try:
    from blist import blist as list
except ImportError:
    pass
try:
    from functools import total_ordering
except ImportError:
    from total_ordering import total_ordering
import operator

from .interval import coerce_interval, Interval


@total_ordering
class IntervalSet(object):
    def __init__(self, intervals):
        if isinstance(intervals, IntervalSet):
            self.intervals = intervals.intervals
            return
        try:
            self.intervals = list(intervals)
        except TypeError:
            self.intervals = [intervals]
        self.intervals = [Interval(interval) for interval in self.intervals]
        self.simplify()

    @classmethod
    def _union_continuous_non_empty(cls, first, second):
        if not (first & second).empty:
            return True
        return (
            (first.upper_inc or second.lower_inc) and
            first.upper == second.lower and
            not first.empty or
            not second.empty
        )

    def simplify(self):
        if not self.intervals:
            return
        self.intervals.sort(key=operator.attrgetter('lower', 'upper'))
        current = self.intervals.pop(0)
        new_intervals = []
        while self.intervals:
            next = self.intervals.pop(0)
            if self._union_continuous_non_empty(current, next):
                current = current | next
            else:
                if not current.empty:
                    new_intervals.append(current)
                current = next
        if not current.empty:
            new_intervals.append(current)
        self.intervals = new_intervals

    @coerce_interval
    def __and__(self, other):
        """
        Define the intersection operator
        """
        return self.__class__((
            interval & other_interval
            for interval in self.intervals
            for other_interval in other.intervals
        ))

    @coerce_interval
    def __or__(self, other):
        """
        Define the union operator
        """
        return self.__class__(self.intervals + other.intervals)

    def __str__(self):
        return ', '.join((str(interval) for interval in self.intervals))

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    def __eq__(self, other):
        return self.intervals == other.intervals

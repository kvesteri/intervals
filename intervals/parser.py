from collections import Iterable
import six


strip = lambda a: a.strip()


class IntervalParser(object):
    def parse_object(self, obj):
        return obj.lower, obj.upper, obj.lower_inc, obj.upper_inc

    def parse_string(self, value):
        if ',' not in value:
            return self.parse_hyphen_range(value)
        else:
            return self.parse_bounded_range(value)

    def parse_sequence(self, seq):
        lower, upper = seq
        if isinstance(seq, tuple):
            return lower, upper, False, False
        else:
            return lower, upper, True, True

    def parse_single_value(self, value):
        return value, value, True, True

    def parse_bounded_range(self, value):
        values = value.strip()[1:-1].split(',')
        lower, upper = map(strip, values)
        return lower, upper, value[0] == '[', value[-1] == ']'

    def parse_hyphen_range(self, value):
        values = value.split('-')
        if len(values) == 1:
            lower = upper = value.strip()
        else:
            lower, upper = map(strip, values)
        return lower, upper, True, True

    def __call__(self, bounds, lower_inc=None, upper_inc=None):
        if isinstance(bounds, six.string_types):
            values = self.parse_string(bounds)
        elif isinstance(bounds, Iterable):
            values = self.parse_sequence(bounds)
        elif hasattr(bounds, 'lower') and hasattr(bounds, 'upper'):
            values = self.parse_object(bounds)
        else:
            values = self.parse_single_value(bounds)
        values = list(values)
        if lower_inc is not None:
            values[2] = lower_inc
        if upper_inc is not None:
            values[3] = upper_inc
        return values

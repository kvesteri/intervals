from .exc import IntervalException

strip = lambda a: a.strip()


class IntervalStringParser(object):
    def parse_string(self, value):
        if ',' not in value:
            return self.parse_hyphen_range(value)
        else:
            return self.parse_bounded_range(value)

    def parse_bounded_range(self, value):
        values = value.strip()[1:-1].split(',')
        lower, upper = map(strip, values)
        return (
            [lower, upper],
            value[0] == '[',
            value[-1] == ']'
        )

    def parse_hyphen_range(self, value):
        """
        Parse hyphen ranges such as: 2 - 5, -2 - -1, -3 - 5
        """
        values = value.strip().split('-')
        values = list(map(strip, values))
        if len(values) == 1:
            lower = upper = value.strip()
        elif len(values) == 2:
            lower, upper = values
            if lower == '':
                # Parse range such as '-3'
                upper = '-' + upper
                lower = upper
        else:
            if len(values) > 4:
                raise IntervalException(
                    'Unknown interval format given.'
                )
            values_copy = []
            for key, value in enumerate(values):
                if value != '':
                    try:
                        if values[key - 1] == '':
                            value = '-' + value
                    except IndexError:
                        pass
                    values_copy.append(value)
            lower, upper = values_copy

        return [lower, upper], True, True


class IntervalParser(object):
    def parse_object(self, obj):
        return obj.lower, obj.upper, obj.lower_inc, obj.upper_inc

    def parse_sequence(self, seq):
        lower, upper = seq
        if isinstance(seq, tuple):
            return lower, upper, False, False
        else:
            return lower, upper, True, True

    def parse_single_value(self, value):
        return value, value, True, True

    def __call__(self, bounds, lower_inc=None, upper_inc=None):
        if isinstance(bounds, (list, tuple)):
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

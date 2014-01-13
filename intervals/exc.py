class IntervalException(Exception):
    pass


class RangeBoundsException(IntervalException):
    def __init__(self, min_value, max_value):
        self.message = 'Min value %s is bigger than max value %s.' % (
            min_value,
            max_value
        )

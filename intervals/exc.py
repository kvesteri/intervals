class IntervalException(Exception):
    pass


class RangeBoundsException(IntervalException):
    def __init__(self, min_value, max_value):
        super(RangeBoundsException, self).__init__(
            'Min value %s is bigger than max value %s.' % (
                min_value,
                max_value
            )
        )


class IllegalArgument(IntervalException):
    def __init__(self, message):
        super(IntervalException, self).__init__(message)

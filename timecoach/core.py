from datetime import timedelta
from dateutil.relativedelta import relativedelta
from functools import reduce

INTERVAL_NAMES_SINGULAR = [
    'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'
]

INTERVAL_NAMES_PLURAL = [
    'years', 'months', 'days', 'hours', 'minutes', 'seconds', 'microseconds'
]

INTERVAL_ROUNDING_VALUES = {
    'month': 1,
    'day': 1,
    'hour': 0,
    'minute': 0,
    'second': 0,
    'microsecond': 0,
}

INTERVAL_FACTOR = {
    'seconds': 60,  # in a minute
    'minutes': 60,  # in an hour
    'hours': 24,  # in a day
    'days': None,
    'months': 12,
    'years': None,
}

INTERVAL_CHUNKING_TIMEDELTAS = {
    'years': lambda x: relativedelta(years=+x),
    'months': lambda x: relativedelta(months=+x),
    'days': lambda x: timedelta(days=x),
    'hours': lambda x: timedelta(hours=x),
    'minutes': lambda x: timedelta(minutes=x),
    'seconds': lambda x: timedelta(seconds=x)
}


def chunk(start, end, **interval):

    assert start < end

    interval_keys = list(interval.keys())

    assert len(interval) > 0, 'missing arg `interval_key` is required'
    assert len(interval
               ) == 1, 'cannot have more than one interval_key level: {}'.format(
                   interval_keys)

    interval_key = interval_keys[0]
    interval_value = interval[interval_key]
    interval_idx = INTERVAL_NAMES_PLURAL.index(interval_key)

    chunking_interval_name = INTERVAL_NAMES_PLURAL[interval_idx]
    chunking_timedelta = INTERVAL_CHUNKING_TIMEDELTAS[chunking_interval_name](
        interval_value)

    # get list of all interval_key names at indices deeper than `interval_idx`
    rounding_interval_names = INTERVAL_NAMES_SINGULAR[interval_idx + 1:]
    rounding = {}

    rounding_interval_name = INTERVAL_NAMES_SINGULAR[interval_idx]

    # build a rounding dict, similar to:
    # {'minute': 0, 'second': 0, 'microsecond': 0}
    for interval_name in rounding_interval_names:
        rounding[interval_name] = INTERVAL_ROUNDING_VALUES[interval_name]


    interval_factor = INTERVAL_FACTOR[interval_key]

    if interval_factor is not None and interval_value > 1:
        interval_indices = int(interval_factor / interval_value)
        interval_steps = [i * interval_value for i in range(interval_indices)]

        start_interval_value = getattr(start, rounding_interval_name)
        
        closest_step = reduce(
            lambda _closest_step, a_step: a_step if start_interval_value >= a_step else _closest_step,
            interval_steps, 0)

        rounding[rounding_interval_name] = closest_step


    chunk_start = start

    while (chunk_start < end):

        if start is chunk_start:
            
            # round down the leading chunk's start datetime and add an hour to get its end datetime
            
            # NOTE: rounding handles potential edge case where leading chunk's start datetime is between hours

            chunk_end = chunk_start.replace(**rounding) + chunking_timedelta
        
        else:
            
            # incrememt the middle chunks
            
            chunk_end = chunk_start + chunking_timedelta

        
        if (chunk_end > end):
            
            # ceil the trailing chunk's end datetime
            # NOTE: ceiling handles potential edge case where trailing chunk's end datetime is between hours
            
            chunk_end = end

        yield chunk_start, chunk_end

        # prep start datetime for next chunk in loop
        chunk_start = chunk_end


def closest(lst, K):

    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

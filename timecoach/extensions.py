from .core import chunk

def chunk_years(start, end):
    return chunk(start, end, years=1)


def chunk_months(start, end):
    return chunk(start, end, months=1)


def chunk_days(start, end):
    return chunk(start, end, days=1)


def chunk_hours(start, end):
    return chunk(start, end, hours=1)


def chunk_minutes(start, end):
    return chunk(start, end, minutes=1)


def chunk_seconds(start, end):
    return chunk(start, end, seconds=1)

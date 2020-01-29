from datetime import timedelta, datetime, timezone
from functools import reduce

class TimeCoachChunk:

  def __init__(self, chunk_start, chunk_end):

    assert chunk_start < chunk_end

    self.start = chunk_start
    self.end = chunk_end

    self.diff = chunk_end - chunk_start

    self.net_hours = self.diff.seconds / 3600

    self.net_hours_rounded = round(self.net_hours, 2)

def iter_chunks(a_datetime, b_datetime, chunker):
    return [
        TimeCoachChunk(start, end)
        for start, end in chunker(a_datetime, b_datetime)
    ]

def total_hours(chunks):
    return reduce(lambda hours, chunk: hours + chunk.net_hours, chunks, 0)

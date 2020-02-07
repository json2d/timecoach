# ⏳ timecoach
a utility library for generating chunks of **time** within a datetime range

## Installation

```bash
pip install timecoach
```

## Quick Start

here's how to iterate through chunks of **iso hours** using `timecoach.chunk_hours`:

```py
import timecoach
import datetime

start = datetime.datetime(2020, 1, 11, 12, 30, 0) # 12:30pm on January 11th 2020
end = datetime.timedelta(hours=2) # two hours later

for chunk_start, chunk_end in timecoach.chunk_hours(start, end)
  diff = chunk_end - chunk_start
  print("i'm a {} minute time chunk!".format(diff.minutes))

# i'm a 30 minute time chunk!
# i'm a 60 minute time chunk!
# i'm a 30 minute time chunk!
```

and other common chunk sizes:

```py
timecoach.chunk_seconds(start, end) 
timecoach.chunk_minutes(start, end) 
timecoach.chunk_hours(start, end)
timecoach.chunk_days(start, end)
timecoach.chunk_months(start, end)
timecoach.chunk_years(start, end)
```

to specify a custom chunk size:

```py
timecoach.chunk(start, end, minutes=15) # quarter hours 
timecoach.chunk(start, end, hours=12) # half days 
timecoach.chunk(start, end, months=3) # quarter years
```

there are a few caveat with custom chunk sizes:
- the chunk interval must be divisible by its parent interval
- the chunk interval must be defined with a single interval type 
- the chunk interval value must be a non-zero positive integer

for example the following would throw exceptions:

```py
timecoach.chunk(start, end, minutes=13)
# AssertionError:  13 minutes is not divisible by parent interval 1 hours (60 minutes)

timecoach.chunk(start, end, hours=1, minutes=15)
# AssertionError: 1 hours 15 minutes does not contain only one interval type

timecoach.chunk(start, end, hour=.25)
# AssertionError: .25 hours is not non-zero positive integer interval value

timecoach.chunk(start, end, hour=-1)
# AssertionError: .25 hours is not non-zero positive integer interval value

```

if your chunk interval type is `year` then sky's the limit since its the highest interval:

```py
timecoach.chunk(start_of_time, now, years=1000000) # every million years since the start of time
```

## License
MIT

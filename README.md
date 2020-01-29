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

the caveat with this is that the chunk size needs to be divisible by its parent interval.

for example the following would be invalid:

```py
timecoach.chunk(minutes=13)
# AssertionError: 1 hour / 60 minutes is not divisible by 13 minutes
```

if your chunk interval is `year` then sky's the limit since its the highest interval:

```py
timecoach.chunk(start_of_time, now, years=1000000) # every million years since the start of time
```

## License
MIT

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from datetime import timedelta, datetime, timezone
from dateutil import parser as dateparser
from helpers import TimeCoachChunk, iter_chunks, total_hours
import timecoach

from functools import reduce

import unittest

class TestEverything(unittest.TestCase):

    # use `_test` prefix isntead of `test` (w/o leading underscore) so test runner doesn't use it
    def _test_common(self, a_datetime, b_datetime, chunks):
        # leading chunk start datetime is equal to range start date
        self.assertEqual(a_datetime, chunks[0].start)

        # trailing chunk end datetime is equal to range end date
        self.assertEqual(b_datetime, chunks[-1].end)

        middle_chunk_hours = None
        # all middle chunks should have the same duration
        for i in range(len(chunks)):
            is_middle_chunk = i > 0 and i < len(chunks) - 1

            if is_middle_chunk:
                if middle_chunk_hours is None:
                    middle_chunk_hours = chunks[i].net_hours
                else:
                    self.assertEqual(chunks[i].net_hours, middle_chunk_hours)

    def test_15_minute_chunks_with_45_minutes(self):

        a_datetime = dateparser.parse('1-1-90 11:15:00')
        b_datetime = a_datetime + timedelta(minutes=45)

        chunks = [
            TimeCoachChunk(start, end)
            for start, end in timecoach.chunk(a_datetime, b_datetime, minutes=15)
        ]

        self.assertEqual(len(chunks), 3)
        self.assertEqual(total_hours(chunks), .75)
        self._test_common(a_datetime, b_datetime, chunks)

        a_datetime = dateparser.parse('1-1-90 11:35:00')
        b_datetime = a_datetime + timedelta(minutes=45)

        chunks = [
            TimeCoachChunk(start, end)
            for start, end in timecoach.chunk(a_datetime, b_datetime, minutes=15)
        ]

        self.assertEqual(len(chunks), 4)
        self.assertEqual(total_hours(chunks), .75)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_half_hour(self):

        a_datetime = dateparser.parse('1-1-90 11:15:00')
        b_datetime = a_datetime + timedelta(minutes=30)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(total_hours(chunks), .5)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_half_hour_leap(self):

        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime + timedelta(minutes=30)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 2)
        self.assertEqual(total_hours(chunks), .5)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_hour(self):

        a_datetime = dateparser.parse('1-1-90 11:00:00')
        b_datetime = a_datetime + timedelta(hours=1)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(total_hours(chunks), 1)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_hour_leap(self):

        a_datetime = dateparser.parse('1-1-90 11:15:00')
        b_datetime = a_datetime + timedelta(hours=1)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 2)
        self.assertEqual(total_hours(chunks), 1)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_hour_and_half(self):

        a_datetime = dateparser.parse('1-1-90 11:00:00')
        b_datetime = a_datetime + timedelta(hours=1, minutes=30)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))       

        self.assertEqual(len(chunks), 2)
        self.assertEqual(total_hours(chunks), 1.5)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_hour_and_half_leap(self):

        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime + timedelta(hours=1, minutes=30)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 3)
        self.assertEqual(total_hours(chunks), 1.5)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_day(self):

        a_datetime = dateparser.parse('1-1-90 11:00:00')
        b_datetime = a_datetime + timedelta(days=1)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 24)
        self.assertEqual(total_hours(chunks), 24)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_day_leap(self):

        a_datetime = dateparser.parse('1-1-90 11:15:00')
        b_datetime = a_datetime + timedelta(days=1)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_hours))

        self.assertEqual(len(chunks), 25)
        self.assertEqual(total_hours(chunks), 24)
        self._test_common(a_datetime, b_datetime, chunks)

    def test_week(self):

        a_datetime = dateparser.parse('1-1-90 11:15:00')
        b_datetime = a_datetime + timedelta(days=7)

        chunks = list(iter_chunks(a_datetime, b_datetime, timecoach.chunk_days))

        self.assertEqual(len(chunks), 8)
        self.assertEqual(chunks[4].diff.days, 1)

    def test_half_year(self):

        a_datetime = dateparser.parse('1-15-90 12:00:00')
        b_datetime = a_datetime + timedelta(days=6 * 30)

        chunks = list(
            iter_chunks(a_datetime, b_datetime, timecoach.chunk_months))
        self.assertEqual(len(chunks), 7)
        self.assertEqual(chunks[0].diff.days, 16)
        self.assertEqual(chunks[0].diff.seconds, 12 * 3600)
        self.assertEqual(chunks[2].diff.days, 31)  # 31 days in May

    def test_time_travel(self):

        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime - timedelta(
            minutes=30)  # going backwards in time

        with self.assertRaises(AssertionError):
            list(timecoach.chunk_hours(
                a_datetime, b_datetime))  # using `list` to call iterator

    def test_no_time_delta(self):
        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime  # start and end datetime are equal

        with self.assertRaises(AssertionError):
            list(timecoach.chunk_hours(
                a_datetime, b_datetime))  # using `list` to call iterator

    def test_no_non_positive_intervals(self):
        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime + timedelta(days=1)

        weird_intervals = [dict(seconds=-10), dict(minutes=0), dict(hours=-999)]
        
        for interval in weird_intervals:
            with self.assertRaises(AssertionError):
                list(timecoach.chunk(
                    a_datetime, b_datetime, **interval))  # using `list` to call iterator
                     
    def test_no_indivisible_intervals(self):
        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime + timedelta(days=1)

        weird_intervals = [dict(seconds=51), dict(minutes=11), dict(hours=3)]
        
        for interval in weird_intervals:
            with self.assertRaises(AssertionError):
                list(timecoach.chunk(
                    a_datetime, b_datetime, **interval))  # using `list` to call iterator
                     
    def test_no_floaty_intervals(self):

        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime - timedelta(
            minutes=30)  # going backwards in time

        weird_intervals = [dict(seconds=.5), dict(minutes=3.14), dict(hours=.9999)]
        
        for interval in weird_intervals:        
            with self.assertRaises(AssertionError):
                list(timecoach.chunk(
                    a_datetime, b_datetime, **interval))  # using `list` to call iterator
              
    def test_no_multitype_intervals(self):
        a_datetime = dateparser.parse('1-1-90 11:45:00')
        b_datetime = a_datetime + timedelta(days=1)  # start and end datetime are equal

        with self.assertRaises(AssertionError):
            list(timecoach.chunk(
                a_datetime, b_datetime, minutes=11, hours=2))  # using `list` to call iterator                


unittest.main()

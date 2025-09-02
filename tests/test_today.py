import unittest
import datetime

from handling.today import find_today_money

class TestToday(unittest.TestCase):

    def test_find_today_money(self):
        

        startdate = datetime.date(2024, 1, 10)
        enddate = datetime.date(2024, 1, 19)
        today = datetime.date(2024, 1, 15)
        budget = 100
        sum = 30.75

        today_left = find_today_money(startdate, enddate, today, budget, sum)
        
        self.assertEquals(today_left, 29.25)
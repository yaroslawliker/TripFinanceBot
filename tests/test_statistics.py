import unittest
import datetime

from handling.statistics import split_into_weeks

from entities import Expense

class TestToday(unittest.TestCase):

    def test_split_into_weeks_edges(self):
        
        weeks_init = [
            [Expense(0, 0, datetime.datetime(2025, 11, 1), None, 0)],

            [
                Expense(0, 0, datetime.datetime(2025, 11, 3), None, 0),
                Expense(0, 0, datetime.datetime(2025, 11, 7), None, 0)
            ],

            [
                Expense(0, 0, datetime.datetime(2025, 11, 11), None, 0),
                Expense(0, 0, datetime.datetime(2025, 11, 16), None, 0)
            ],
            
            [Expense(0, 0, datetime.datetime(2025, 11, 23), None, 0)],

            [Expense(0, 0, datetime.datetime(2025, 11, 24), None, 0)],
        ]

        expenses = [expense for expenses in weeks_init for expense in expenses]

        weeks_result = split_into_weeks(expenses)
        
        self.assertEqual(weeks_init, weeks_result)

    def test_split_into_weeks_skipped(self):
        
        weeks_init = [
            [Expense(0, 0, datetime.datetime(2025, 11, 3), None, 0)],
            [Expense(0, 0, datetime.datetime(2025, 11, 30), None, 0)]
        ]

        expenses = [expense for expenses in weeks_init for expense in expenses]

        weeks_result = split_into_weeks(expenses)

        weeks_init.insert(1, [])
        weeks_init.insert(1, [])
        
        self.assertEqual(weeks_init, weeks_result)
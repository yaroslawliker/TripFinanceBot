import unittest
import datetime

from handling.statistics import init_week_edges, split_into_weeks, WeekExpensesDTO, calculate_week_total_expense
from entities import Expense

class TestWeekSorting(unittest.TestCase):

    def test_init_week_edges_basic(self):
        start = datetime.date(2025, 11, 3)
        end   = datetime.date(2025, 11, 26)

        weeks = init_week_edges(start, end)

        self.assertEqual(len(weeks), 4)

        expected = [
            (datetime.date(2025, 11, 3),  datetime.date(2025, 11, 9)),
            (datetime.date(2025, 11, 10), datetime.date(2025, 11, 16)),
            (datetime.date(2025, 11, 17), datetime.date(2025, 11, 23)),
        ]

        for week, (exp_start, exp_end) in zip(weeks, expected):
            self.assertEqual(week.week_start, exp_start)
            self.assertEqual(week.week_end, exp_end)

    def test_split_into_weeks(self):
        start = datetime.date(2025, 11, 1)
        end   = datetime.date(2025, 11, 26)

        weeks = init_week_edges(start, end)

        # Create test expenses
        e1 = Expense(1, 10, datetime.datetime(2025, 11, 1), None, 0)
        e2 = Expense(2, 20, datetime.datetime(2025, 11, 7), None, 0)
        e3 = Expense(3, 30, datetime.datetime(2025, 11, 13), None, 0)
        e4 = Expense(3, 30, datetime.datetime(2025, 11, 16), None, 0)
        e5 = Expense(4, 40, datetime.datetime(2025, 11, 26), None, 0)

        expenses = [e1, e2, e3, e4, e5]

        split_into_weeks(expenses, weeks)

        self.assertEqual(weeks[0].expenses, [e1])
        self.assertEqual(weeks[1].expenses, [e2])
        self.assertEqual(weeks[2].expenses, [e3, e4])
        self.assertEqual(weeks[3].expenses, [])
        self.assertEqual(weeks[4].expenses, [e5])

    def test_calculation_statistics(self):
        
        # --- Creating weeks ---
        # First week
        start_1 = datetime.date(2025, 11, 1)
        end_1 = datetime.date(2025, 11, 8)
        
        exp1 = Expense(1, 100.5, datetime.datetime(2025, 11, 2), "Food", 1)
        exp2 = Expense(2, 50.0, datetime.datetime(2025, 11, 3), "Taxi", 1)
        
        week_1_dto = WeekExpensesDTO(start_1, end_1, [exp1, exp2])

        # Second week
        start_2 = datetime.date(2025, 11, 8)
        end_2 = datetime.date(2025, 11, 11)
        
        week_2_dto = WeekExpensesDTO(start_2, end_2, [])

        weeks_input = [week_1_dto, week_2_dto]

        # Act
        stats = calculate_week_total_expense(weeks_input)
        
        self.assertEqual(len(stats), 2)

        # First week
        self.assertEqual(stats[0].days, 7)
        self.assertAlmostEqual(stats[0].total, 150.5) 

        # Second week
        self.assertEqual(stats[1].days, 3)
        self.assertEqual(stats[1].total, 0.0)



if __name__ == "__main__":
    unittest.main()

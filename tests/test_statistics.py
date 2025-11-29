import unittest
import datetime

from handling.statistics.model import init_week_edges, split_into_weeks, \
    WeekExpensesDTO, calculate_week_total_expense, \
    get_expenses_of_weekday, calculate_weekdays_evarage
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
            self.assertEqual(week.start, exp_start)
            self.assertEqual(week.end, exp_end)

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
        start_1 = datetime.date(2025, 11, 3)
        end_1 = datetime.date(2025, 11, 9)
        
        exp1 = Expense(1, 100.5, datetime.datetime(2025, 11, 4), "Food", 1)
        exp2 = Expense(2, 50.0, datetime.datetime(2025, 11, 5), "Taxi", 1)
        
        week_1_dto = WeekExpensesDTO(start_1, end_1, [exp1, exp2])

        # Second week
        start_2 = datetime.date(2025, 11, 10)
        end_2 = datetime.date(2025, 11, 12)
        
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
    
    def test_get_expenses_of_weekday(self):

        e1 = Expense(1, 130, datetime.datetime(2025, 11, 26), None, -1)
        e2 = Expense(2, 50, datetime.datetime(2025, 11, 26), None, -1)
        e3 = Expense(3, 25, datetime.datetime(2025, 11, 27), None, -1)

        week = WeekExpensesDTO(
            datetime.date(2025, 11, 24),
            datetime.date(2025, 11, 30),
            [e1, e2, e3]
        )

        wed = get_expenses_of_weekday(week, 2)
        thu = get_expenses_of_weekday(week, 3)
        fri = get_expenses_of_weekday(week, 4)

        self.assertEqual([e1, e2], wed)
        self.assertEqual([e3], thu)
        self.assertEqual([], fri)
    
    def test_get_expenses_of_weekday_not_full_week(self):

        e1 = Expense(1, 130, datetime.datetime(2025, 11, 26), None, -1)
        e2 = Expense(2, 50, datetime.datetime(2025, 11, 26), None, -1)
        e3 = Expense(3, 25, datetime.datetime(2025, 11, 27), None, -1)

        week = WeekExpensesDTO(
            datetime.date(2025, 11, 26),
            datetime.date(2025, 11, 28),
            [e1, e2, e3]
        )

        mon = get_expenses_of_weekday(week, 0)
        tue = get_expenses_of_weekday(week, 1)
        wed = get_expenses_of_weekday(week, 2)
        thu = get_expenses_of_weekday(week, 3)
        fri = get_expenses_of_weekday(week, 4)
        sat = get_expenses_of_weekday(week, 5)
        sun = get_expenses_of_weekday(week, 6)

        self.assertEqual([e1, e2], wed)
        self.assertEqual([e3], thu)
        self.assertEqual([], fri)
        self.assertEqual(None, mon)
        self.assertEqual(None, tue)
        self.assertEqual(None, sat)
        self.assertEqual(None, sun)

    def test_calculate_weekdays_average(self):

        e1 = Expense(1, 130, datetime.datetime(2025, 11, 26), None, -1) # Wed
        e2 = Expense(2, 50, datetime.datetime(2025, 11, 26), None, -1) # Wed
        e3 = Expense(3, 25, datetime.datetime(2025, 11, 27), None, -1) # Thu

        week1 = WeekExpensesDTO(
            datetime.date(2025, 11, 26),
            datetime.date(2025, 11, 28),
            [e1, e2, e3]
        )

        e4 = Expense(1, 45, datetime.datetime(2025, 12, 1), None, -1) # Mon
        e5 = Expense(2, 15.5, datetime.datetime(2025, 12, 3), None, -1) # Wed
        e6 = Expense(3, 25.3, datetime.datetime(2025, 12, 4), None, -1) # Thu

        week2 = WeekExpensesDTO(
            datetime.date(2025, 12, 1),
            datetime.date(2025, 12, 4),
            [e4, e5, e6]
        )
        expected = [
            e4.money,
            0,
            (e1.money + e2.money + e5.money) / 3,
            (e3.money + e6.money) / 2,
            0,
            0,
            0
        ]

        # Act
        weeks = [week1, week2]
        result = calculate_weekdays_evarage(weeks)

        # Assert
        self.assertEqual(expected, result)




if __name__ == "__main__":
    unittest.main()

import unittest
import datetime
import unittest.mock

from handling.week import calculate_budget_per_day, calculate_day_of_week, calculate_period_budget, calculate_view_data
from entities import Category, Expense
from logic.category_expense_calculator import CategoryExpenseInfoDTO


class TestWeekHandler(unittest.TestCase):

    def test_calculate_budget_per_day(self):

        startdate = datetime.date(2024, 1, 10)
        enddate = datetime.date(2024, 1, 19)
        budget = 100

        per_day = calculate_budget_per_day(startdate, enddate, budget)

        self.assertAlmostEqual(per_day, 10.0)

    def test_calculate_day_of_week(self):

        start_date = datetime.date(2025, 10, 7)  # Tuesday

        monday = datetime.date(2025, 10, 6)
        thursday = datetime.date(2025, 10, 9)
        sunday = datetime.date(2025, 10, 12)

        self.assertEqual(calculate_day_of_week(start_date, 0), monday)
        self.assertEqual(calculate_day_of_week(start_date, 1), start_date)
        self.assertEqual(calculate_day_of_week(start_date, 3), thursday)
        self.assertEqual(calculate_day_of_week(start_date, 6), sunday)

    def test_calculate_period_budget(self):

        startdate = datetime.date(2024, 1, 10)
        enddate = datetime.date(2024, 1, 14)
        per_day = 10.5

        period_budget = calculate_period_budget(startdate, enddate, per_day)

        self.assertAlmostEqual(period_budget, 10.5 * 5)

    def test_calculate_view_data(self):
        
        # Prepare mocks
        message = unittest.mock.MagicMock()
        database = unittest.mock.MagicMock()
        expense_calculator = unittest.mock.MagicMock()

        # Preparing test data
        start_date1 = datetime.date(2024, 4, 10)
        end_date1 = datetime.date(2024, 4, 25)
        budget1 = 16*20
        spend1 = 140.25

        today1_1 = datetime.date(2024, 4, 13)
        must_left1_1 = 5*20-spend1
        week_bugdet1_1 = 5*20

        today1_2 = datetime.date(2024, 4, 18)
        must_left1_2 = 12*20-spend1
        week_budget1_2 = 7*20

        today1_3 = datetime.date(2024, 4, 23)
        must_left1_3 = 16*20-spend1
        week_budget1_3 = 4*20

        start_date2 = datetime.date(2024, 9, 25)
        end_date2 = datetime.date(2024, 10, 29)
        budget2 = 35*5
        today2 = datetime.date(2024, 10, 29)
        week_budget2 = 2*5

        message.chat.id = 1
        categories = [
            Category(id=1, name="Food", budget=budget1, start_date=start_date1, end_date=end_date1, user_id=1),
            Category(id=2, name="Transport", budget=budget2, start_date=start_date2, end_date=end_date2, user_id=1)
        ]
        database.get_categories.return_value = categories

        infoDTOs = [
            CategoryExpenseInfoDTO("Food", budget1, spend1),
            CategoryExpenseInfoDTO("Transport", budget2, 0)
        ]
        expense_calculator.calculate_categories_expenses.return_value = infoDTOs

        # Act1 for 1
        view_data = calculate_view_data(message, today1_1, database, expense_calculator)

        # Assert
        self.assertEqual(len(view_data), 1) # One becaouse today is out of period
        self.assertEqual(view_data[0].category_name, "Food")

        self.assertAlmostEqual(view_data[0].week_budget, week_bugdet1_1)  # Budget for this week only
        self.assertAlmostEqual(view_data[0].week_left, must_left1_1)

        # Act1 for 2
        view_data = calculate_view_data(message, today1_2, database, expense_calculator)

        # Assert
        self.assertAlmostEqual(view_data[0].week_budget, week_budget1_2)  # Budget for this week only
        self.assertAlmostEqual(view_data[0].week_left, must_left1_2)

        # Act1 for 3
        view_data = calculate_view_data(message, today1_3, database, expense_calculator)

        # Assert
        self.assertAlmostEqual(view_data[0].week_budget, week_budget1_3)  # Budget for this week only
        self.assertAlmostEqual(view_data[0].week_left, must_left1_3)

        view_data = calculate_view_data(message, today2, database, expense_calculator)

        # Act for 2
        self.assertEqual(view_data[0].category_name, "Transport")
        self.assertAlmostEqual(view_data[0].week_budget, week_budget2)  # Budget for this week only





import unittest
from unittest.mock import MagicMock
from entities import Category, Expense
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO

class TestCategoryExpenseCalculator(unittest.TestCase):

    def setUp(self):
        self.mock_database = MagicMock()
        self.calculator = CategoryExpenseCalculator(self.mock_database)

    def test_calculate_category_expense(self):
        # Arrange
        category_id = 1
        mock_expenses = [MagicMock(money=50), MagicMock(money=30), MagicMock(money=20)]
        self.mock_database.get_expenses.return_value = mock_expenses

        # Act
        total_expense = self.calculator.calculate_category_expense(category_id)

        # Assert
        self.assertEqual(total_expense, 100)
        self.mock_database.get_expenses.assert_called_once_with(category_id)

    def test_calculate_categories_expenses(self):
        # Arrange
        categories = [
            Category(id=1, name="Food", budget=200, start_date=None, end_date=None, user_id=1),
            Category(id=2, name="Transport", budget=150, start_date=None, end_date=None, user_id=1)
        ]
        
        self.mock_database.get_categories.return_value = categories
        self.mock_database.get_expenses.side_effect = [
            [MagicMock(money=50), MagicMock(money=30)],  # Expenses for category 1
            [MagicMock(money=40)]  # Expenses for category 2
        ]

        # Act
        result = self.calculator.calculate_categories_expenses(categories)

        # Assert
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].name, "Food")
        self.assertEqual(result[0].budget, 200)
        self.assertEqual(result[0].left, 120)

        self.assertEqual(result[1].name, "Transport")
        self.assertEqual(result[1].budget, 150)
        self.assertEqual(result[1].left, 110)

        self.mock_database.get_expenses.assert_any_call(1)
        self.mock_database.get_expenses.assert_any_call(2)

if __name__ == '__main__':
    unittest.main()
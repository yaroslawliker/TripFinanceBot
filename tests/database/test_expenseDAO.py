import unittest
import datetime
import sqlite3
from database.daos.expenseDAO import ExpenseDAO, Expense
from database.sql_loader import load_sql_from_file

class TestUserDAO(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.expenseDAO = ExpenseDAO(self.conn)

        CREATE_USERS_QUERY = load_sql_from_file("users.sql")
        self.conn.execute(CREATE_USERS_QUERY)
        CREATE_CATEGORY_QUERY = load_sql_from_file("categories.sql")
        self.conn.execute(CREATE_CATEGORY_QUERY)

        CREATE_EXPENSES_QUERY = load_sql_from_file("expenses.sql")
        self.conn.execute(CREATE_EXPENSES_QUERY)

    def test_add_expense(self):
        expense = Expense(None, 123.45, datetime.datetime(2025, 10, 5, 14, 30), "Test purpose", 1)
        self.expenseDAO.add(expense)

        cursor = self.conn.execute("SELECT * FROM expenses WHERE money = ?", (expense.money,))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[1], expense.money)
        self.assertEqual(row[2], expense.datetime.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(row[3], expense.purpose)
        self.assertEqual(row[4], expense.category_id)

    def test_get_expenses_by_category_id__no_expenses(self):
        result = self.expenseDAO.get_all_by_category(1)
        expected = []

        self.assertEqual(expected, result)

    def test_get_expenses_by_category_id__with_expenses(self):
        expenses = [
            Expense(None, 50.0, datetime.datetime(2025, 10, 1, 10, 0), "Expense 1", 2),
            Expense(None, 75.5, datetime.datetime(2025, 10, 2, 12, 30), "Expense 2", 2),
            Expense(None, 20.25, datetime.datetime(2025, 10, 3, 15, 45), "Expense 3", 2)
        ]

        for expense in expenses:
            self.expenseDAO.add(expense)

        result = self.expenseDAO.get_all_by_category(2)

        self.assertEqual(len(expenses), len(result))

        for i in range(len(expenses)):
            expected = expenses[i]
            self.assertEqual(expected.money, result[i].money)
            self.assertEqual(expected.datetime, result[i].datetime)
            self.assertEqual(expected.purpose, result[i].purpose)
            self.assertEqual(expected.category_id, result[i].category_id)
    
    
    def tearDown(self):
        self.conn.close()
        self.conn = None
        self.categoryDAO = None




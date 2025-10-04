import unittest
import datetime
import sqlite3
from database.daos.categoryDAO import CategoryDAO, Category
from database.sql_loader import load_sql_from_file

class TestUserDAO(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.categoryDAO = CategoryDAO(self.conn)

        CREATE_USERS_QUERY = load_sql_from_file("users.sql")
        self.conn.execute(CREATE_USERS_QUERY)
        CREATE_CATEGORY_QUERY = load_sql_from_file("categories.sql")
        self.conn.execute(CREATE_CATEGORY_QUERY)
    
    def test_category_from_row(self):
        row = [1234, "Cool category", 300, "2025-09-29", "2026-10-13", 5678]
        expected = Category(1234, "Cool category", 300, datetime.date(2025, 9, 29), datetime.date(2026, 10, 13), 5678)

        result = CategoryDAO._from_row(row)

        self.assertEqual(expected.id, result.id)
        self.assertEqual(expected.name, result.name)
        self.assertEqual(expected.budget, result.budget)
        self.assertEqual(expected.start_date, result.start_date)
        self.assertEqual(expected.end_date, result.end_date)
        self.assertEqual(expected.chat_id, result.chat_id)
    
    def test_category_from_row__no_dates(self):
        row = [1234, "Cool category", 300, None, None, 5678]
        expected = Category(1234, "Cool category", 300, None, None, 5678)

        result = CategoryDAO._from_row(row)

        self.assertEqual(expected.id, result.id)
        self.assertEqual(expected.name, result.name)
        self.assertEqual(expected.budget, result.budget)
        self.assertEqual(expected.start_date, result.start_date)
        self.assertEqual(expected.end_date, result.end_date)
        self.assertEqual(expected.chat_id, result.chat_id)

    def test_add_category(self):
        category = Category(None, "New category", 400, None, None, 1234)
        self.categoryDAO.add(category)

        cursor = self.conn.execute("SELECT * FROM categories WHERE name = ?", (category.name,))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[1], category.name)
        self.assertEqual(row[2], category.budget)
        self.assertEqual(row[5], category.chat_id)
    
    def test_get_all_categories_of_user__no_categories(self):
        result = self.categoryDAO.get_all_by_user(1234)
        expected = []

        self.assertEqual(expected, result)
    
    def test_get_all_categories_of_user__some_categories(self):
        categories = [
            Category(None, "Category 1", 100, None, None, 1234),
            Category(None, "Category 2", 200, None, None, 1234),
            Category(None, "Category 3", 300, None, None, 5678)
        ]

        for category in categories:
            self.categoryDAO.add(category)
        
        result = self.categoryDAO.get_all_by_user(1234)
        expected = [
            Category(1, "Category 1", 100, None, None, 1234),
            Category(2, "Category 2", 200, None, None, 1234)
        ]

        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i].id, result[i].id)
            self.assertEqual(expected[i].name, result[i].name)
            self.assertEqual(expected[i].budget, result[i].budget)
            self.assertEqual(expected[i].start_date, result[i].start_date)
            self.assertEqual(expected[i].end_date, result[i].end_date)
            self.assertEqual(expected[i].chat_id, result[i].chat_id)

    def test_get_category_by_user_and_name__no_category(self):
        result = self.categoryDAO.get_by_user_and_name("Nonexistent", 1234)
        self.assertIsNone(result)
    
    def test_get_category_by_user_and_name__exists(self):
        category = Category(None, "Category 1", 100, None, None, 1234)
        self.categoryDAO.add(category)

        result = self.categoryDAO.get_by_user_and_name("Category 1", 1234)
        expected = Category(1, "Category 1", 100, None, None, 1234)

        self.assertIsNotNone(result)
        self.assertEqual(expected.id, result.id)
        self.assertEqual(expected.name, result.name)
        self.assertEqual(expected.budget, result.budget)
        self.assertEqual(expected.start_date, result.start_date)
        self.assertEqual(expected.end_date, result.end_date)
        self.assertEqual(expected.chat_id, result.chat_id)
    
    def test_update_category(self):
        category = Category(None, "Category 1", 100, None, None, 1234)
        self.categoryDAO.add(category)

        category_to_update = Category(1, "Updated Category", 500, datetime.date(2025, 10, 1), datetime.date(2025, 12, 31), 1234)
        self.categoryDAO.update(category_to_update)

        cursor = self.conn.execute("SELECT * FROM categories WHERE id = ?", (1,))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], category_to_update.id)
        self.assertEqual(row[1], category_to_update.name)
        self.assertEqual(row[2], category_to_update.budget)
        self.assertEqual(row[3], "2025-10-01")
        self.assertEqual(row[4], "2025-12-31")
        self.assertEqual(row[5], category_to_update.chat_id)

    def tearDown(self):
        self.conn.close()
        self.conn = None
        self.categoryDAO = None




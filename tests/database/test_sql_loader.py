import unittest
import database.sql_loader

class Test_sql_loader(unittest.TestCase):

    def setUp(self):
        database.sql_loader.SQL_FILDER_PATH = "tests/database/"

    def test_load_sql_from_file__no_file(self):
        self.assertRaises(
            FileNotFoundError,
            lambda: 
                database.sql_loader.load_sql_from_file("no-existing-file.sql")
        )
    
    def test_load_sql_from_file__file_exists(self):
        result = database.sql_loader.load_sql_from_file("users_test_table.sql")
        expected = """CREATE TABLE users {
    chat_id PRIMARY KEY INTEGER
}"""

        self.assertEqual(expected, result)

    
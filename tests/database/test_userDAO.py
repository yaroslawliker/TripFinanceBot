import unittest
import sqlite3
from database.daos.userDAO import UserDAO
from entities import User
from database.sql_loader import load_sql_from_file



class TestUserDAO(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.userDAO = UserDAO(self.conn)

        CREATE_USERS_QUERY = load_sql_from_file("users.sql")
        self.conn.execute(CREATE_USERS_QUERY)
    
    def test_is_user_exists__no_user(self):
        self.assertFalse(self.userDAO.is_exists(1234))

    def test_is_user_exists__after_adding(self):
        id = 5678
        user = User(id)
        self.userDAO.add(user)

        self.assertFalse(self.userDAO.is_exists(1234))
        self.assertTrue(self.userDAO.is_exists(id))

    def tearDown(self):
        self.conn.close()
        self.conn = None
        self.userDAO = None
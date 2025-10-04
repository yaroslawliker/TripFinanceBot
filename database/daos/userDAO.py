import sqlite3

from entities import User
from database.daos.genericDAO import GenericDAO

class UserDAO(GenericDAO):

    def add(self, user: User):
        chat_id = user.chat_id
        self._connection.execute("INSERT INTO users(chat_id) VALUES (?)", (chat_id,))
    
    def is_exists(self, chat_id:int) -> bool:
        cursor = self._connection.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        res = cursor.fetchall()
        return len(res) != 0


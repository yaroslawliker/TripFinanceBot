import sqlite3

from entities import User
from database.genericDAO import GenericDAO

class UserDAO(GenericDAO):

    def add_user(self, user: User):
        chat_id = user.chat_id
        self.__connection.execute("INSERT ? INTO users", (chat_id,))
    
    def is_user_exists(self, chat_id:int) -> bool:
        cursor = self.__connection.execute("SELECT * FROM users WHERE user = ?", (chat_id,))
        res = cursor.fetchall()
        return len(res) != 0


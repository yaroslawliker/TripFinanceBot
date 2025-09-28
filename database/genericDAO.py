import sqlite3

class GenericDAO:
    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection

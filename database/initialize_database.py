import sqlite3
from database.sql_loader import load_sql_from_file

TABLES = ['users', 'categories', 'expenses']

def ensure_database_initialized(connection: sqlite3.Connection):

    if not is_database_initialized(connection):
        initialize_database(connection)

def is_database_initialized(connection: sqlite3.Connection) -> bool:
    cursor = connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    existin_tables = [row[0] for row in cursor.fetchall()]

    for table in TABLES:
        if table not in existin_tables:
            return False
    return True

def initialize_database(connection: sqlite3.Connection):

    for table in TABLES:
        print("Creating table:", table)
        connection.execute(load_sql_from_file(table + '.sql'))
    
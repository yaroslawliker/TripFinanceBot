import sqlite3

def run_migration():
    connection = sqlite3.connect("database.db")
    add_category_archived(connection)
    connection.close()
    
def add_category_archived(connection):
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE categories ADD COLUMN archived INTEGER DEFAULT 0")
    connection.commit()

if __name__ == "__main__":
    run_migration()
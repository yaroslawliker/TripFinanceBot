import json
import sqlite3
import datetime

from entities import User, Category, Expense
from database.daos import UserDAO, CategoryDAO, ExpenseDAO
from database.initialize_database import ensure_database_initialized

def run_migration():
    connection = sqlite3.connect("database.db")
    ensure_database_initialized(connection)
    from_json_to_sqlite(connection)

def from_json_to_sqlite(connection):

    user_dao = UserDAO(connection)
    category_dao = CategoryDAO(connection)
    expense_dao = ExpenseDAO(connection)

    with open('database.json', 'rt') as file:
        data = json.load(file)

    for chat_id in data:
        user_data = data[chat_id]
        user = User(int(chat_id))
        user_dao.add(user)

        categories = user_data['categories']

        for category_name in categories:
            category_data = categories[category_name]

            if 'startdate' in category_data:
                startdate = str_to_date(category_data['startdate'])
                enddate = str_to_date(category_data['enddate'])
            else:
                startdate = None
                enddate = None

            category = Category(
                None,
                category_name,
                category_data['budget'],
                startdate,
                enddate,
                chat_id
            )
            category_dao.add(category)

            category_id = category_dao.get_by_user_and_name(category_name, chat_id).id

            for expense_data in category_data['transactions']:
                expense = Expense(
                    None,
                    expense_data['money'],
                    ExpenseDAO.str_to_datetime(expense_data['datetime']),
                    None,
                    category_id
                )
                
                expense_dao.add(expense)

    connection.commit()
    connection.close()

def str_to_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
                
if __name__ == "__main__":
    run_migration()
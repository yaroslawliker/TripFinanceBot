from database.daos.genericDAO import GenericDAO
from entities import Expense


class ExpenseDAO(GenericDAO):

    def _from_row(row):
        """ Creates Expense object from the given row from a database """
        id = row[0]
        money = row[1]
        datetime = GenericDAO.str_to_datetime(row[2])
        purpose = row[3]
        category_id = row[4]

        return Expense(id, money, datetime, purpose, category_id)
    
    def add(self, expense: Expense):
        """ 
        Adds a new expense from the given. 
        The id field is ignored, new id is stored in the database 
        """
        self._connection.execute(
            "INSERT INTO expenses(money, datetime, purpose, category_id) VALUES (?, ?, ?, ?)",
            (expense.money, expense.datetime, expense.purpose, expense.category_id)
        )
    
    def get_by_category_id(self, category_id: int) -> list:
        expenses = []

        result = self._connection.execute(
            "SELECT * FROM expenses WHERE category_id = ?", (category_id,)
        ).fetchall()

        for row in result:
            expenses.append(ExpenseDAO._from_row(row))

        return expenses
    
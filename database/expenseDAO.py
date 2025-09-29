from database.genericDAO import GenericDAO
from entities import Expense


class ExpenseDAO(GenericDAO):

    def _expense_from_row(row):
        id = row[0]
        money = row[1]
        datetime = GenericDAO.str_to_datetime(row[2])
        purpose = row[3]
        category_id = row[4]

        return Expense(id, money, datetime, purpose, category_id)
    
    def add_expense(self, expense: Expense):
        self._connection.execute(
            "INSERT INTO expenses(money, datetime, purpose, category_id) VALUES (?, ?, ?, ?)",
            (expense.money, expense.datetime, expense.purpose, expense.category_id)
        )
    
    def get_expenses_by_category_id(self, category_id: int) -> list:
        expenses = []

        result = self._connection.execute(
            "SELECT * FROM expenses WHERE category_id = ?", (category_id,)
        ).fetchall()

        for row in result:
            expenses.append(ExpenseDAO._expense_from_row(row))

        return expenses
    
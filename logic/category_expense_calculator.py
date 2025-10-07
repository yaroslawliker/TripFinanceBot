
from database.database_service import DatabaseService

class CategoryExpenseInfoDTO:
    def __init__(self, name: str, budget: float, spent: float):
        self.name = name
        self.budget = budget
        self.spent = spent
        self.left = budget - spent

class CategoryExpenseCalculator:
    """ Service that calculates total expenses for a given category. """

    def __init__(self, database: DatabaseService):
        self._database = database

    def calculate_category_expense(self, category_id):
        """ 
        Calculates total expense for a given category.
        total = sum([expense1, expense2...])
        """
        expenses = self._database.get_expenses(category_id)

        sum = 0
        for expense in expenses:
            sum += expense.money
        return sum

    def calculate_categories_expenses(self, user_id):
        """Takes user_id as input. Returns list of CategoryExpenseInfoDTO of the given user."""
        categories = self._database.get_categories(user_id)
        result = []
        for category in categories:

            total_expense = self.calculate_category_expense(category.id)

            result.append(CategoryExpenseInfoDTO(category.name, category.budget, total_expense))
            
        return result
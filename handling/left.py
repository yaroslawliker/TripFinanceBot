from database.database_service import DatabaseService
from messages import Messages
from entities import Category, Expense # Needed for type hints during development

TOTALS_KEY = "totals"

class CategoryExpenseInfoDTO:
    def __init__(self, name: str, budget: float, left: float):
        self.name = name
        self.budget = budget
        self.left = left

def calculate_total_expenses(expenses):
    
    sum = 0
    for expense in expenses:
        sum += expense.money
    return sum

def calculate_totals(categories, database: DatabaseService):
    """Takes categories list and database service as input. Returns list of CategoryExpenseInfoDTO."""
    result = []
    for category in categories:

        expenses = database.get_expenses(category.id)
        total_expense = calculate_total_expenses(expenses)

        left = category.budget - total_expense

        result.append(CategoryExpenseInfoDTO(category.name, category.budget, left))
        
    return result

def handle_left(message, bot, database: DatabaseService):

    categories = database.get_categories(message.chat.id)
    
    infoDTOs = calculate_totals(categories, database)
    
    result = Messages.STATS_MONEY_LEFT

    for infoDTO in infoDTOs:
        infoDTO: CategoryExpenseInfoDTO
        
        result += "{0}:  {1} / {2}\n".format(
            infoDTO.name, 
            round(infoDTO.left, 2), 
            round(infoDTO.budget,2)
        )

    bot.send_message(message.chat.id, result)




        
        
        




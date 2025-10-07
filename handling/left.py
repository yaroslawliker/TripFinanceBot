from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO
from messages import Messages
from entities import Category, Expense # Needed for type hints during development

TOTALS_KEY = "totals"

def handle_left(message, bot, database: DatabaseService,  expense_calculator: CategoryExpenseCalculator):
   
    categories = database.get_categories(message.chat.id)
    infoDTOs = expense_calculator.calculate_categories_expenses(categories)
    
    result = Messages.STATS_MONEY_LEFT

    for infoDTO in infoDTOs:
        infoDTO: CategoryExpenseInfoDTO
        
        result += "{0}:  {1} / {2}\n".format(
            infoDTO.name, 
            round(infoDTO.left, 2), 
            round(infoDTO.budget,2)
        )

    bot.send_message(message.chat.id, result)




        
        
        




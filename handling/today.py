import datetime

from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO
from messages import Messages
from entities import Category, Expense # Needed for type hints during development

def find_today_money(startdate, enddate, today, budget, total_expense) -> float:
    
    if today > enddate or today < startdate:
        return None

    delta_full = enddate - startdate
    days_full = delta_full.days + 1

    delta_today = today - startdate
    days_today = delta_today.days + 1

    # All the meth
    today_left = (budget / days_full) * days_today  - total_expense

    return today_left


def handle_today(message, bot, database: DatabaseService, expense_calculator: CategoryExpenseCalculator):

    # Check if parameters after /today exists
    if len(message.text) > 6:
        bot.send_message(message.chat.id, Messages.TODAY_WRONG_USAGE)
        return

    categories = database.get_categories(message.chat.id)
    infoDTOs = expense_calculator.calculate_categories_expenses(categories)
    
    result = "Today you have:\n"
    for category, infoDTO in zip(categories, infoDTOs):
        category: Category
        infoDTO: CategoryExpenseInfoDTO

        # Skip if no dates are set up
        if category.start_date is None:
            continue

        startdate = category.start_date
        enddate = category.end_date
        
        today = datetime.datetime.now().date()

        today_left = find_today_money(startdate, enddate, today, category.budget, infoDTO.spent)

        if today_left is None:
            result += f"{category.name}: out of period\n"
        else:       
            result += f"{category.name}: {round(today_left, 2)}\n"

    bot.send_message(message.chat.id, result)

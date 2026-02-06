from handling._args import extract_args
from database.database_service import DatabaseService
from messages import Messages
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO

def handle_check_archive(message, bot,
                         database_service: DatabaseService, 
                         category_expense_calculator: CategoryExpenseCalculator
                         ):
    arguments = extract_args(message.text)

    try:
        if (len(arguments) != 0):
            raise IndexError()
        
        user_id = message.chat.id

        # Ensuring the category exists and getting it's id
        categories = database_service.get_archived_categories(user_id)
        categoryExpenseInfos = category_expense_calculator.calculate_categories_expenses(categories)

        # Building the answer string
        view = view_check_archive(categoryExpenseInfos)
        bot.send_message(message.chat.id, view)

    except IndexError:
        bot.send_message(message.chat.id, Messages.CHECK_ARCHIVE_WRONG_USAGE)

def view_check_archive(categories: list) -> str:

    if (len(categories) == 0):
        return Messages.NO_ARCHIVED_CATEGORIES
    
    result = Messages.ARCHIVED_CATEGORIES
    for category in categories:
        category: CategoryExpenseInfoDTO
        result += f"{category.name}: {round(category.left, 2)} / {round(category.budget, 2)}\n"
    
    return result



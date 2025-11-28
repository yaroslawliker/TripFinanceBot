from messages import Messages
from handling._args import extract_args
from database.database_service import DatabaseService, NoSuchCategoryExistsException, ExpenseIsNotInTheCategory


def handle_canes_spend(message, bot, database_service: DatabaseService):
    arguments = extract_args(message.text)

    try:
        # Parsing arguments
        category = arguments[0]
        expense_id = int(arguments[1])

        # Ensuring the category exists and getting it's id
        category = database_service.get_category(message.chat.id, category)
        
        # Deleting the expense
        database_service.delete_expense_if_in_category(expense_id, category.id)

        bot.send_message(message.chat.id, Messages.CANCEL_SPEND_DELETED)

    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except ExpenseIsNotInTheCategory:
        bot.send_message(message.chat.id, Messages.CANCEL_SPEND_NO_SUCH.format(expense_id, category))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, Messages.CANCEL_SPEND_WRONG_USAGE)
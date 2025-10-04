from messages import Messages
from database.database_service import DatabaseService, CategoryAlreadyExistsException
from handling._args import extract_args

def handle_add(message, bot, database_service: DatabaseService):
    arguments = extract_args(message.text)

    if len(arguments) < 1 or len(arguments) > 2:
        bot.send_message(message.chat.id, Messages.ADD_ARGUMENT_ERROR)
        return
    
    category = arguments[0]
    if len(arguments) > 1:
        try:
            budget = float(arguments[1])
        except ValueError:
            bot.send_message(message.chat.id, Messages.ADD_ARGUMENT_ERROR)
            return
        except CategoryAlreadyExistsException:
            bot.send_message(message.chat.id, Messages.CATEGORY_ALREADY_EXISTS.format(category))
            return
    else:
        budget = 0

    database_service.add_category(message.chat.id, category, budget)
    bot.send_message(message.chat.id, Messages.ADD_CATEGORY_CREATED.format(category, budget))
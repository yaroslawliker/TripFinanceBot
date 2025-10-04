from messages import Messages
import database_service as database
from handling._args import extract_args

def handle_add(message, bot):
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
        except database.CategoryAlreadyExistsException:
            bot.send_message(message.chat.id, Messages.CATEGORY_ALREADY_EXISTS.format(category))
    else:
        budget = 0

    bot.send_message(message.chat.id, Messages.ADD_CATEGORY_CREATED.format(category, budget))
    database.add_category(message.chat.id, category, budget)
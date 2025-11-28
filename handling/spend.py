from database.database_service import DatabaseService, NoSuchCategoryExistsException
from messages import Messages
from handling._args import extract_args

def handle_spend(message, bot, database: DatabaseService):
    arguments = extract_args(message.text)
    
    try:
        category = arguments[0]
        money = float(arguments[1])

        if (len(arguments) > 2):
            purpose = ' '.join(arguments[2:])
        else:
            purpose = None

        database.add_expense(message.chat.id, category, money, purpose)
        bot.send_message(message.chat.id, Messages.SPEND_SUCCESS.format(category, money))
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, Messages.SPEND_ARGUMENT_ERROR)
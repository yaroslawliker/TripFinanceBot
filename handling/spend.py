import database.database_service as database
from messages import Messages
from handling._args import extract_args

def handle_spend(message, bot):
    arguments = extract_args(message.text)
    
    try:
        category = arguments[0]
        money = float(arguments[1])
        database.add_transaction(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.SPEND_SUCCESS.format(category, money))
    except database.NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, Messages.SPEND_ARGUMENT_ERROR)
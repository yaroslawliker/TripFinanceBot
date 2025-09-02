from database_service import DatabaseService, NoSuchCategoryExistsException
from messages import Messages

def handle_spend(message, bot):
    command = message.text[7:]
    arguments = command.split(" ")
    try:
        category = arguments[0]
        money = float(arguments[1])
        DatabaseService.add_transaction(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.SPEND_SUCCESS.format(category, money))
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, Messages.SPEND_ARGUMENT_ERROR)
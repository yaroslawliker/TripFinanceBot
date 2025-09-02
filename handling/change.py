import database_service as database
from messages import Messages

def handle_change(message, bot):
    command = message.text[8:]
    arguments = command.split(" ")
    try:
        category = arguments[0]
        money = float(arguments[1])
        database.change_budget(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.CHANGE_SUCCESS.format(category, money))
    except database.NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, Messages.CHANGE_ARGUMENT_ERROR)
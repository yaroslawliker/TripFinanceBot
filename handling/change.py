from messages import Messages
from handling._args import extract_args
from database.database_service import DatabaseService, NoSuchCategoryExistsException, CategoryIsArchivedException

def handle_change(message, bot, database_service: DatabaseService):
    arguments = extract_args(message.text)

    try:
        category = arguments[0]
        money = float(arguments[1])
        database_service.change_budget(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.CHANGE_SUCCESS.format(category, money))
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except CategoryIsArchivedException:
        bot.send_message(message.chat.id, Messages.CATEGORY_IS_ARCHIVED.format(category))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, Messages.CHANGE_ARGUMENT_ERROR)
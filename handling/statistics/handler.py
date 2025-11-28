from database.database_service import DatabaseService, NoSuchCategoryExistsException
from handling._args import extract_args, ArgumentError

from messages import Messages
from handling.statistics.model import get_model
from handling.statistics.view import view_statistics



def handle_statistics(message, bot, database: DatabaseService):
    try:
        arguments = extract_args(message.text)

        category = arguments[0]
        if len(arguments) > 1:
            raise ArgumentError("Wrong amount of arguments")
        
        # Model
        model = get_model(message.chat.id, category, database)

        # View
        view_statistics(bot, message.chat.id, category, model)

    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, Messages.STATS_WRONG_USAGE)
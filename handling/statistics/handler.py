from database.database_service import DatabaseService
from handling._args import extract_args, ArgumentError

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

    except Exception as e:
        raise e
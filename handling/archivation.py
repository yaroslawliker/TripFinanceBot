from handling._args import extract_args
from database.database_service import DatabaseService, NoSuchCategoryExistsException, ArchivatedIsAsUpdatedException
from messages import Messages

def handle_archivate(message, bot, database_service: DatabaseService):
    _handle_archived_generic(message, bot, database_service, True)

def handle_unarchivate(message, bot, database_service: DatabaseService):
    _handle_archived_generic(message, bot, database_service, False)


def _handle_archived_generic(message, bot, database_service: DatabaseService, archived: bool):
    arguments = extract_args(message.text)

    archived_command = "archive" if archived else "unarchive"
    archived_word = archived_command + "d"

    try:
        # Parsing arguments
        category_name = arguments[0]

        # Ensuring the category exists and getting it's id

        # Archivate the category
        if (archived):
            database_service.archivate(message.chat.id, category_name)
        else:
            database_service.unarchivate(message.chat.id, category_name)

        bot.send_message(message.chat.id, Messages.ARCHIVATE_SUCCESS.format(category_name, archived_word))

    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category_name))
    except ArchivatedIsAsUpdatedException:
        bot.send_message(message.chat.id, Messages.ARCHIVATE_IS_ALREADY_ARCHIVATED.format(category_name, archived_word))
    except IndexError:
        bot.send_message(message.chat.id, Messages.ARCHIVATE_WRONG_USAGE.format(archived_command))

        


class Messages():
    """Class contains all text messages"""

    HELP = "This is a bot for managing money in travel.\n"

    ADD_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/add Transfer 150"
    ADD_CATEGORY_CREATED = "Category '{0}' created with budget {1}"
    CATEGORY_ALREADY_EXISTS = "Category '{0}' already exists."

    NO_SUCH_CATEGORY = "Category '{0}' haven't been created yet."

    CHANGE_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/change Transfer 175"
    CHANGE_SUCCESS = "{0}'s budged was changed to {1}."

    SPEND_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/spend Transfer 7.5"
    SPEND_SUCCESS = "Spent {1} money on {0}."

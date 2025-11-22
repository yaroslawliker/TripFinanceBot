

class Messages():
    """Class contains all text messages"""

    HELP = """This is a bot for managing money in travel.
/add <category> - add spending category
/change <category> <amount> - change the budget of the category\n
/spend <category> <amount> - spend money to the category
/left - check how much money left of every category
"""

    ADD_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/add Transfer 150"
    ADD_CATEGORY_CREATED = "Category '{0}' created with budget {1}"
    CATEGORY_ALREADY_EXISTS = "Category '{0}' already exists."

    NO_SUCH_CATEGORY = "Category '{0}' haven't been created yet."

    CHANGE_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/change Transfer 175"
    CHANGE_SUCCESS = "{0}'s budged was changed to {1}."

    SPEND_ARGUMENT_ERROR = "Wrong usage. Correct example:\n/spend Transfer 7.5"
    SPEND_SUCCESS = "Spent {1} money on {0}."

    STATS_MONEY_LEFT = "Money left:\n"

    SET_DATES_ORDER_ERROR = "Wrong usage. Start of the period must be before end of the period."
    SET_DATES_SUCCESS = "Period start and finish are set up"
    SET_DATES_EXAMPLE = "Wrong usage. Example:\n/setdates Transfer 10.01.2024 17.01.2024"

    TODAY_WRONG_USAGE = "Wrong usage. Just write '/today'"

    SPENDS_WRONG_USAGE = "Wrong usage. Correct example:\n/spends Transfer"
    SPENDS_HEADER = "Spend data for {0}"
    SPENDS_EMPTY = "No spends yet. You can write down them with /spend command."
    SPENDS_TABLE_COLUMNS = "ID. money date{0} time purpose"
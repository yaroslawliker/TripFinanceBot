

class Messages():
    """Class contains all text messages"""

    HELP = """This is a bot for managing money in travel.
Main commands:
/add <category> - add spending category
/change <category> <amount> - change the budget of the category
/spend <category> <amount> - spend money in the category
/spends <category> - check the list of spends in the category
/left - check how much money left of every category

Smart money monitoring
/setdates <category> <start date> <end date> - set the date borders of your category
/today - check the money, apportioned for today
/week - check the money, approtioned for this week

/superhelp - more detailed explanation
"""

    SUPERHELP = """<b>Superhelp</b>
This is a bot for splitting money on budgets, keeping track of spends and spread money across periods.

<b>Main commands:</b>
/add &lt;category&gt; &lt;~budget&gt; - add spending category with the given budget. If budget is not written, it is set to 0
Categories are needed to devide different spends: for example in a trip as an example you may have this categories: Transfer, Hotels, Food, EntryTickets ect.

/change &lt;category&gt; &lt;amount&gt; - change the budget of the category
/spend &lt;category&gt; &lt;amount&gt; - spend money in the category.
You will later be able to see your spend list and statistics.

/spends &lt;category&gt; - check the list of spends in the category in the table format: ID. money | date time | purpose (if persent)
If all spends have the same year, the year is ommited.

/left - check how much money left of every category
For each category: left = budget - sum(spends)

<b>Smart money monitoring</b>
/setdates &lt;category&gt; &lt;start date&gt; &lt;end date&gt; - set the date borders of your category
The date format should be dd.mm.yyyy, for example 29.12.2025.

/today - check the money, apportioned for today.
To use this command you first have to /setdates of your category.
This commands helps check how much money you have, if the budged were devided for the period, set with /setdates.
In other words, if your today`s balance is positive, this means you may spend this amount today, and you are keeping with the budged.\
If your today`s budget is negative, probably, you have spent too much.
For each category: today = budget/period*thisDayNum - sum(spends), where
- period is number of days from start-date to end-date
- thisDayNum is the number of the day, counting from the period`s start-date till and including today.

/week - check the money, approtioned for this week, in the simmilar way as /today.
It accounts that the first or the last weeks of the periods may be less then 7 days.
Intuitively, your week`s balance, is how much you can spend till the end of this week to keep yourself within the budget.
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
    SPENDS_HEADER = "Spends list for '{0}'"
    SPENDS_EMPTY = "No spends yet. You can write down them with /spend command."
    SPENDS_YEAR = "All dates are within {0} year"
    SPENDS_TABLE_COLUMNS = "ID.  money  |  date time  |  purpose"
import datetime

import handling.left as left
import database_service as database
from messages import Messages

def find_today_money(startdate, enddate, today, budget, sum) -> float:
    
    if today > enddate or today < startdate:
        return None

    delta_full = enddate - startdate
    days_full = delta_full.days + 1

    delta_today = today - startdate
    days_today = delta_today.days + 1

    # All the meth
    today_left = (budget / days_full) * days_today  - sum

    return today_left


def handle_today(message, bot):

    if len(message.text) > 6:
        bot.send_message(message.chat.id, Messages.TODAY_WRONG_USAGE)
        return

    categories = database.get_categories(message.chat.id)
    totals = left.calculate_totals(categories)
    
    result = "Today you have:\n"
    for key in totals:

        # Getting dates from db
        dates = database.get_dates(message.chat.id, key)
        # Skip if no dates are set up
        if dates is None:
            continue

        startdate = dates[database.STARTDATE_KEY]
        enddate = dates[database.ENDDATE_KEY]
        
        today = datetime.datetime.now().date()

        # Getting currect category sum and budget
        total = totals[key]
        sum = total[left.TOTALS_KEY]
        budget = total[database.BUDGET_KEY]

        today_left = find_today_money(startdate, enddate, today, budget, sum)

        if today_left is None:
            result += f"{key}: out of period\n"
        else:       
            result += f"{key}: {round(today_left, 2)}\n"

    bot.send_message(message.chat.id, result)

import database.database_service as database
from messages import Messages

TOTALS_KEY = "totals"

def calculate_total_spend(category):
    transactions = category[database.TRANSACTIONS_KEY]
    sum = 0
    for transaction in transactions:
        sum += transaction[database.MONEY_KEY]
    return sum

def calculate_totals(categories:dict):
    """Takes categories dict and returns dict with category names as keys and 'totals' and 'budget' keys"""
    result = {}
    for key in categories.keys():
        result[key] = {
            TOTALS_KEY:calculate_total_spend(categories[key]),
            database.BUDGET_KEY: categories[key][database.BUDGET_KEY]
        }
    return result

def get_fromatted_stats(message, bot):

    categories = database.get_categories(message.chat.id)
    
    sums = calculate_totals(categories)
    
    result = Messages.STATS_MONEY_LEFT
    for key in sums:
        stats = sums[key]
        budget = stats[database.BUDGET_KEY]
        left = budget - stats[TOTALS_KEY]
        result += "{0}:  {1} / {2}\n".format(key, round(left, 2), round(budget,2))

    bot.send_message(message.chat.id, result)




        
        
        




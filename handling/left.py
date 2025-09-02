from database_service import DatabaseService
from messages import Messages

TOTALS_KEY = "totals"

def calculate_total_spend(category):
    transactions = category[DatabaseService.TRANSACTIONS_KEY]
    sum = 0
    for transaction in transactions:
        sum += transaction[DatabaseService.MONEY_KEY]
    return sum

def calculate_totals(categories:dict):
    """Takes categories dict and returns dict with category names as keys and 'totals' and 'budget' keys"""
    result = {}
    for key in categories.keys():
        result[key] = {
            TOTALS_KEY:calculate_total_spend(categories[key]),
            DatabaseService.BUDGET_KEY: categories[key][DatabaseService.BUDGET_KEY]
        }
    return result

def get_fromatted_stats(categories):
    
    sums = calculate_totals(categories)
    
    result = Messages.STATS_MONEY_LEFT
    for key in sums:
        stats = sums[key]
        budget = stats[DatabaseService.BUDGET_KEY]
        left = budget - stats[TOTALS_KEY]
        result += "{0}:  {1} / {2}\n".format(key, round(left, 2), round(budget,2))

    return result




        
        
        




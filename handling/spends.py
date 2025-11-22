from datetime import datetime

from database.database_service import DatabaseService, NoSuchCategoryExistsException
from messages import Messages
from handling._args import extract_args


def handle_spends(message, bot, database: DatabaseService):
    try:
        # Extracting arguments
        arguments = extract_args(message.text)
        category = arguments[0]
        
        print(arguments)

        if len(arguments) > 1:
            raise ValueError(f"Message have to much arguments, one expected, got {len(arguments)}.")
    
        # Getting model
        expenses = get_expenses(message.chat.id, category, database)
        
        # Building view
        view = view_spends_data(category, expenses)
        # Sending with a controller
        bot.send_message(message.chat.id, view)

    except NoSuchCategoryExistsException as e:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, Messages.SPENDS_WRONG_USAGE)


###
### Model function
###

def get_expenses(user_id: int, category_name: str, database: DatabaseService):
    category = database.get_category(user_id, category_name)
    return database.get_expenses(category.id)

###
### View functions
###

def view_spends_data(category_name, expenses):
    
    msg = Messages.SPENDS_HEADER.format(category_name) + '\n'
    
    # Empty case
    if len(expenses) == 0:
        msg += Messages.SPENDS_EMPTY
        return msg
    
    # Data is not empty case
    same_year = None
    if is_same_year(expenses):
        same_year = expenses[0].datetime.year
    msg += Messages.SPENDS_TABLE_COLUMNS.format(same_year if same_year is not None else "")
                   
    for expense in expenses:
        msg += str(expense.id) + ". "
        msg += str(expense.money) + " "
        
        # Date and time
        if same_year is not None:
            msg += expense.datetime.strftime("%d.%m %H:%M") + " "
        else:
            msg += expense.datetime.strftime("%d.%m.%Y %H:%M") + " "
        
        if expense.purpose is not None:
            msg += expense.purpose
            
        msg += "\n" 
    
    return msg
     
def is_same_year(expenses):
    year = expenses[0].datetime.year
    for expense in expenses:
        if year != expense.datetime.year:
            return False
    return True


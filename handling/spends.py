from database.database_service import DatabaseService, NoSuchCategoryExistsException
from messages import Messages
from handling._args import extract_args

from entities import Expense


def handle_spends(message, bot, database: DatabaseService):
    try:
        # Extracting arguments
        arguments = extract_args(message.text)
        category = arguments[0]
        
        if len(arguments) > 1:
            raise ValueError(f"Message have to much arguments, one expected, got {len(arguments)}.")
    
        # Getting model
        expenses = get_expenses(message.chat.id, category, database)
        
        # Building view
        view = view_spends_data_html(category, expenses)
        # Sending with a controller
        bot.send_message(message.chat.id, view, parse_mode="HTML")

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

def view_spends_data_html(category_name, expenses):
    
    # Msg builder for the whole result
    msg = Messages.SPENDS_HEADER.format(category_name) + '\n'
    
    # Empty case
    if len(expenses) == 0:
        msg += Messages.SPENDS_EMPTY
        return msg
    
    # Data is not empty case
    same_year = None
    if is_same_year(expenses):
        same_year = expenses[0].datetime.year
        msg += Messages.SPENDS_YEAR.format(same_year) + "\n"
        
    # Another str builder for the list
    list_str = ""
    list_str += Messages.SPENDS_TABLE_COLUMNS + "\n"
    
    max_id = get_max_symbols(expenses, lambda expense: expense.id)
    max_money = get_max_symbols(expenses, lambda expense: expense.money)
                       
    for expense in expenses:
        list_str += str(expense.id) + calculate_indent(max_id, expense.id, 1) + "|  "
        
        # Money
        list_str += str(expense.money)
        list_str += calculate_indent(max_money, expense.money, 2) + "|  "
        
        # Date and time
        if same_year is not None:
            date_msg = expense.datetime.strftime("%d.%m %H:%M")
        else:
            date_msg = expense.datetime.strftime("%d.%m.%Y %H:%M")
        list_str += f"{date_msg}"
        
        if expense.purpose is not None:
            list_str += "  |  " + expense.purpose
            
        list_str += "\n" 
        
    msg += surround_with_tag(list_str, "pre")
    
    return msg
     
def is_same_year(expenses):
    year = expenses[0].datetime.year
    for expense in expenses:
        if year != expense.datetime.year:
            return False
    return True

def get_max_symbols(expenses, getter) -> int:
    
    return max(
        [len(str(getter(expense))) for expense in expenses]
    )
    
def calculate_indent(max_symbols, num, min_indent=1) -> str:
    cur_symbols = len(str(num))
    spaces = max_symbols - cur_symbols + min_indent
    return " " * spaces

def surround_with_tag(msg, tag):
    return f"<{tag}>" + msg + f"</{tag}>"
    
    
    
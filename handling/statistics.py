import datetime

from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO
from messages import Messages
from entities import Category, Expense

from handling._args import extract_args, ArgumentError

class NoExpensesException:
    pass

def handle_statistics(message, bot, database: DatabaseService, expense_calculator: CategoryExpenseCalculator):
    try:
        arguments = extract_args(message.text)

        category = arguments[0]
        if len(arguments) > 1:
            raise ArgumentError("Wrong amount of arguments")
        
        model = get_model(message.chat.id, category, database)

    except:
        pass


def get_model(chat_id, category, database: DatabaseService):
    
    category: Category = database.get_category(chat_id, category)
    expenses = database.get_expenses(category.id)

    if len(expenses) == 0:
        raise NoExpensesException

    # Guessing dates of the category
    if category.is_dated():
        start_date = expenses[0].datetime.date()
        end_date = expenses[-1].datetime.date()
        category.start_date = start_date
        category.end_date = end_date
        
    weeks = split_into_weeks(expenses)

def split_into_weeks(expenses):

    weeks = []
    new_week = []
    prev_date = expenses[0].datetime.date()
    for expense in expenses:

        date = expense.datetime.date()
        
        # Calculating the end of previous week
        if (date.weekday() <= prev_date.weekday() and date != prev_date):

            # If a week or few were skipped
            diff = date - prev_date
            if (diff > datetime.timedelta(days=7)):
                # Rolling back to mondays
                prev_mon = prev_date - datetime.timedelta(days=prev_date.weekday())
                this_mon = date    -   datetime.timedelta(days=prev_date.weekday())

                diff = this_mon - prev_mon
                full_weeks = (diff.days-1) // 7
                # Adding empty weeks
                for i in range(full_weeks):
                    weeks.append([])

            weeks.append(new_week)
            new_week = []
        
        prev_date = date
        new_week.append(expense)

    weeks.append(new_week)

    return weeks
    
        
        

    

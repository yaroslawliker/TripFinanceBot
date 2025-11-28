import datetime

from dataclasses import dataclass

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

###
### Model & calculation
###

@dataclass
class WeekExpensesDTO:
    week_start: datetime
    week_end: datetime
    expenses: list

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

        # Checking if the week has been changed
        prev_mon = prev_date - datetime.timedelta(days=prev_date.weekday())
        this_mon = date    -   datetime.timedelta(days=date.weekday())
        diff = this_mon - prev_mon



        # Calculating the end of previous week
        if diff > datetime.timedelta(days=0):
            weeks.append(new_week)

            # If a week or few were skipped
            if (diff > datetime.timedelta(days=8)):

                full_weeks = (diff.days-1) // 7
                # Adding empty weeks
                for i in range(full_weeks):
                    weeks.append([])

            new_week = []
        
        prev_date = date
        new_week.append(expense)

    weeks.append(new_week)

    return weeks
    
        
        

    

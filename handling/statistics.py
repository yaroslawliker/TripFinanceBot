import datetime

from dataclasses import dataclass

from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO
from messages import Messages
from entities import Category, Expense

from handling._args import extract_args, ArgumentError


def handle_statistics(message, bot, database: DatabaseService):
    try:
        arguments = extract_args(message.text)

        category = arguments[0]
        if len(arguments) > 1:
            raise ArgumentError("Wrong amount of arguments")
        
        # Model
        model = get_model(message.chat.id, category, database)

        # View
        view_statistics(bot, message.chat.id, category, model)

    except Exception as e:
        raise e



###
### Model & calculation
###


### Retrieving data

class NoExpensesException:
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

    # Init weeks and split expenses amoung them
    weeks = init_week_edges(start_date, end_date)      
    split_into_weeks(expenses, weeks)

    # Getting week statistics
    stats = calculate_week_total_expense(weeks)
    
    return [(week, stat) for (week, stat) in zip(weeks, stats)]


### Sorting data

@dataclass
class WeekExpensesDTO:
    week_start: datetime
    week_end: datetime
    expenses: list

    def days(self) -> datetime.timedelta:
        return self.week_end - self.week_start

def init_week_edges(start_date:datetime.date, end_date: datetime.date):
    weeks = []

    # Iterating through mondays
    cur_mon = start_date - datetime.timedelta(days=start_date.weekday())
    while(cur_mon <= end_date):

        cur_end = cur_mon + datetime.timedelta(days=6)
        week_dto = WeekExpensesDTO(cur_mon, cur_end, [])
        weeks.append(week_dto)

        cur_mon = cur_mon + datetime.timedelta(days=7)

    # Ensuring edges
    weeks[0].week_start = start_date
    weeks[-1].week_end = end_date

    return weeks

def split_into_weeks(expenses, weeks) -> None:
    """Puts expenses into the appropriate weeks"""

    def update_week(date, cur_week:WeekExpensesDTO, weeks):
        """Updates week"""

        def is_in_week(date, week):
            return date >= week.week_start and date <= week.week_end
        
        if is_in_week(date, cur_week):
            return cur_week
        for week in weeks:
            if is_in_week(date, week):
                return week

    week = weeks[0]
    for expense in expenses:
        week = update_week(expense.datetime.date(), week, weeks)
        week.expenses.append(expense)
    
### Calculating statistics

@dataclass
class WeekStatisicsDTO:
    total: float
    days: float

def calculate_week_total_expense(weeks):
    stats = []

    for week in weeks:
        week: WeekExpensesDTO

        # Getting days amount
        days = (week.week_end - week.week_start).days
        # Getting money sum
        total = sum(map(lambda e: e.money, week.expenses))

        stats.append(WeekStatisicsDTO(total, days))
    
    return stats
        


###
### View functions
###

def view_statistics(bot, chat_id, category, weeks_stats):

    msg = ""

    msg += Messages.STATS_HEADER.format(category)

    start_date = weeks_stats[0][0].week_start
    end_date = weeks_stats[-1][0].week_end
    msg += Messages.STATS_DATES.format(start_date, end_date)

    max_per_day = max([round(stat.total/stat.days,2) for (_, stat) in weeks_stats])

    for i, (week, stat) in enumerate(weeks_stats):

        total = round(stat.total, 2)
        per_day = round(stat.total/stat.days, 2)
        msg += Messages.STATS_WEEK.format(i+1, total, stat.days, per_day)

        if per_day == max_per_day:
            msg += Messages.STATS_MOST_PER_DAY
        
        msg += "\n\n"

    bot.send_message(chat_id, msg, parse_mode="HTML")











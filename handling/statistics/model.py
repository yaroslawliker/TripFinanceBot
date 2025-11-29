"""
Module for retrieving and sorting week expense data and calculation statistics for it.
"""
from dataclasses import dataclass

import datetime
from statistics import mean

from database.database_service import DatabaseService
from entities import Category, Expense


###
### DTOs and expcetion
###

class NoExpensesException:
    pass

@dataclass
class WeekExpensesDTO:
    start: datetime.date
    end: datetime.date
    expenses: list

    def days(self) -> datetime.timedelta:
        return self.end - self.start
    
@dataclass
class WeekStatisicsDTO:
    total: float
    days: float

@dataclass
class StatisticsDTO:
    week_statistics: list # of tuples (WeekExpenseDTO, WeekStatisicsDTO)
    per_day_statistics: list

###
### Retrieving data
###

def get_model(chat_id, category, database: DatabaseService):
    
    category: Category = database.get_category(chat_id, category)
    expenses = database.get_expenses(category.id)

    if len(expenses) == 0:
        raise NoExpensesException

    # Guessing dates of the category
    if not category.is_dated():
        start_date = expenses[0].datetime.date()
        end_date = expenses[-1].datetime.date()
        category.start_date = start_date
        category.end_date = end_date

    # Init weeks and split expenses amoung them
    weeks = init_week_edges(category.start_date, category.end_date)  
    split_into_weeks(expenses, weeks)

    # Getting week statistics
    week_total_expense = calculate_week_total_expense(weeks)
    weeks_stats = [(week, stat) for (week, stat) in zip(weeks, week_total_expense)]

    # Getting per day statistics
    per_day_stats = calculate_weekdays_evarage(weeks)
    
    return StatisticsDTO(
        weeks_stats,
        per_day_stats
    )



###
### Sorting data
###

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
    weeks[0].start = start_date
    weeks[-1].end = end_date

    return weeks

def split_into_weeks(expenses, weeks) -> None:
    """Puts expenses into the appropriate weeks"""

    def update_week(date, cur_week:WeekExpensesDTO, weeks):
        """Updates week"""

        def is_in_week(date, week):
            return date >= week.start and date <= week.end
        
        if is_in_week(date, cur_week):
            return cur_week
        for week in weeks:
            if is_in_week(date, week):
                return week

    week = weeks[0]
    for expense in expenses:
        week = update_week(expense.datetime.date(), week, weeks)
        week.expenses.append(expense)



###
### Calculating statistics
###

### Per week statistics

def calculate_week_total_expense(weeks):
    """Calculates statistics about every week."""
    stats = []

    for week in weeks:
        week: WeekExpensesDTO

        # Getting days amount
        days = (week.end - week.start).days + 1
        # Getting money sum
        total = sum(map(lambda e: e.money, week.expenses))

        stats.append(WeekStatisicsDTO(total, days))
    
    return stats


### Per weekday statistics

def get_expenses_of_weekday(week:WeekExpensesDTO, day_num):
    """
    Gets expenses of the given day.
    day_num is the number of the weekday (0 for monday, 6 for sunday)
    returns the expenses list or None is day is out of the week.
    """

    if week.start.weekday() != 0:
        mon = week.start - datetime.timedelta(days=week.start.weekday())
    else:
        mon = week.start
    day = mon + datetime.timedelta(days=day_num)

    # In case the day is not in the week
    if (day < week.start or day > week.end):
        return None
        
    result = []
    for expense in week.expenses:
        expense: Expense
        if expense.datetime.date() == day:
            result.append(expense)
    return result

def calculate_weekdays_evarage(weeks):
    """Calculates average on every weekday"""

    weekdays_money = [[] for i in range(7)]
    for i in range(7):

        for week in weeks:
            expenses = get_expenses_of_weekday(week, i)
            # The weedays is not in the week (week is not full)
            if expenses == None:
                continue

            if len(expenses) == 0:
                weekdays_money[i].append(0)
            else:
                moneys = [expense.money for expense in expenses]
                weekdays_money[i] += moneys

    averages = [
        mean(day) if len(day) != 0 else 0 
        for day in weekdays_money
    ]

    return averages
            
    
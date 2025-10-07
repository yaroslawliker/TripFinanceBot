from datetime import datetime, timedelta

from entities import Category
from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator, CategoryExpenseInfoDTO

class WeekViewDTO:
    def __init__(self, category_name: str, week_budget: float, week_left: float):
        self.category_name = category_name
        # Only this week budget
        self.week_budget = week_budget
        self.week_left = week_left

def handle_week(message, bot, database: DatabaseService,  expense_calculator: CategoryExpenseCalculator):

    # Separation made for easier testing
    today = datetime.now().date()
    view_data = calculate_view_data(message, today, database, expense_calculator)
    view_week_data(message, bot, view_data)

###
### Calculation functions
###

def calculate_view_data(message, today, database: DatabaseService,  expense_calculator: CategoryExpenseCalculator):
    """ Calculate WeekViewDTO list for every category of the user. """

    view_data = []

    categories = database.get_categories(message.chat.id)
    infoDTOs = expense_calculator.calculate_categories_expenses(categories)
    for category, infoDTO in zip(categories, infoDTOs):
        category: Category
        infoDTO: CategoryExpenseInfoDTO

        # Skip if no dates are set up
        if category.start_date is None:
            continue

        startdate = category.start_date
        enddate = category.end_date
        total_expense = infoDTO.spent
        budget = category.budget

        # Skip if today is out of period
        if today < startdate or today > enddate:
            continue

        per_day = calculate_budget_per_day(startdate, enddate, budget)

        # The last date of the current week (Sunday or enddate)
        last_date = min(calculate_day_of_week(today, 6), enddate)
        # Week budget including prevoius weeks
        week_budget_with_previous = calculate_period_budget(startdate, last_date, per_day)
        left_for_week = week_budget_with_previous - total_expense

        # The first date of the current week (Monday or startdate)
        first_date = max(calculate_day_of_week(today, 0), startdate)
        this_week_only_budget = calculate_period_budget(first_date, last_date, per_day)

        view_data.append(WeekViewDTO(category.name, this_week_only_budget, left_for_week))

    return view_data

def calculate_budget_per_day(startdate: datetime, enddate: datetime, budget: float) -> float:
    delta = enddate - startdate
    days = delta.days + 1
    return budget / days

def calculate_day_of_week(today: datetime, day: int) -> datetime:
    """ Calculate the given day of the week (0 - Monday, 6 - Sunday)"""
    to_day = day - today.weekday()
    delta = timedelta(days=to_day)

    return today + delta

def calculate_period_budget(startdate, enddate, per_day) -> float:
    """ Calculate budget for the given period."""
    delta = enddate - startdate
    days = delta.days + 1
    return per_day * days

###
### Viewer function
###

def view_week_data(message, bot, view_data):

    result = "This week you have:\n"
    for dto in view_data:
        result += f"{dto.category_name}: {round(dto.week_left, 2)} / {round(dto.week_budget, 2)}\n"

    bot.send_message(message.chat.id, result)









    
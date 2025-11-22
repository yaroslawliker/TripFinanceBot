import telebot
import sqlite3

from read_token import read_token

from database.initialize_database import ensure_database_initialized
from database.daos import UserDAO, CategoryDAO, ExpenseDAO
from database.database_service import DatabaseService
from logic.category_expense_calculator import CategoryExpenseCalculator
from messages import Messages

# Import handlers
import handling.change
import handling.set_dates
import handling.spend
import handling.add
import handling.left
import handling.today
import handling.week


###
### Prepare database
###

_connection = sqlite3.connect("database.db", check_same_thread=False, isolation_level=None)
ensure_database_initialized(_connection)

###
### Perform Dependency Injection
###

# Initialize DatabaseService
_userDAO = UserDAO(_connection)
_categoryDAO = CategoryDAO(_connection)
_transactionDAO = ExpenseDAO(_connection)

database_service = DatabaseService(_userDAO, _categoryDAO, _transactionDAO)

# Initialize ExpenseCalculator
expense_calculator = CategoryExpenseCalculator(database_service)

###
### Initialize bot
###

TOKEN = read_token()

bot = telebot.TeleBot(TOKEN, parse_mode=None)

###
### Handlers
###

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.send_message(message.chat.id, Messages.HELP)

@bot.message_handler(commands=["add"])
def add_handler(message):
    handling.add.handle_add(message, bot, database_service)
    
@bot.message_handler(commands=["change"])
def change_handler(message):
    handling.change.handle_change(message, bot, database_service)

@bot.message_handler(commands=["spend"])
def spend_handler(message):
    handling.spend.handle_spend(message, bot, database_service)

@bot.message_handler(commands=["left"])
def left_handler(message):
    handling.left.handle_left(message, bot, database_service, expense_calculator)

@bot.message_handler(commands=["setdates"])
def setdates_handler(message):
    handling.set_dates.handle_set_dates(message, bot, database_service)

@bot.message_handler(commands=["today"])
def today_handler(message):
    handling.today.handle_today(message, bot, database_service, expense_calculator)    

@bot.message_handler(commands=["week"])
def week_handler(message):
    handling.week.handle_week(message, bot, database_service, expense_calculator)



bot.infinity_polling(timeout=3, long_polling_timeout=3)


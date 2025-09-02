import telebot

# Import handlers
import handling.change
import handling.set_dates
import handling.spend
import handling.add
import handling.left
import handling.today

from messages import Messages
from database_service import DatabaseService
from read_token import read_token

TOKEN = read_token()

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.send_message(message.chat.id, Messages.HELP)

@bot.message_handler(commands=["add"])
def add_handler(message):
    handling.add(message, bot)
    
@bot.message_handler(commands=["change"])
def change_handler(message):
    handling.change.handle_change(message, bot)

@bot.message_handler(commands=["spend"])
def spend_handler(message):
    handling.spend.handle_spend(message, bot)

@bot.message_handler(commands=["left"])
def left_handler(message):
    categories = DatabaseService.get_categories(message.chat.id)
    result = handling.left.get_fromatted_stats(categories)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=["setdates"])
def setdates_handler(message):
    handling.set_dates.handle_set_dates(message, bot)

@bot.message_handler(commands=["today"])
def today_handler(message):
    handling.today.handle_today(message, bot)    


bot.infinity_polling()


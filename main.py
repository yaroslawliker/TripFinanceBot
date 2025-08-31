import telebot

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
    command = message.text[5:]
    arguments = command.split(" ")

    if len(arguments) < 1 or len(arguments) > 2:
        bot.send_message(message.chat.id, Messages.ADD_ARGUMENT_ERROR)
        return
    
    category = arguments[0]
    if len(arguments) > 1:
        try:
            budget = int(arguments[1])
        except ValueError:
            bot.send_message(message.chat.id, Messages.ADD_ARGUMENT_ERROR)
            return
    else:
        budget = 0

    bot.send_message(message.chat.id, Messages.ADD_CATEGORY_CREATED.format(category, budget))
    DatabaseService.add_category(message.chat.id, category, budget)

@bot.message_handler(commands=["change"])
def change_handler(message):
    command = message.text[8:]
    arguments = command.split(" ")
    DatabaseService.change_budget(arguments)

bot.infinity_polling()


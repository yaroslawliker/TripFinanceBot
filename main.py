import telebot

from messages import Messages

from read_token import read_token
from add_handling import handle_add

TOKEN = read_token()

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.send_message(message.chat.id, Messages.HELP)

@bot.message_handler(commands=["add"])
def add_handler(message):
    command = message.text[5:]
    arguments = command.split(" ")
    print(message.text)
    print(command)
    print(arguments)
    handle_add(message.chat.id, arguments)

bot.infinity_polling()


import telebot
from read_token import read_token

from messages import Messages
TOKEN = read_token()

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.send_message(message.chat.id, Messages.HELP)

bot.infinity_polling()


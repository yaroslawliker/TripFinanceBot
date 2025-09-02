import datetime
import telebot

from messages import Messages
from database_service import DatabaseService, CategoryAlreadyExistsException, NoSuchCategoryExistsException, StartDaysNotBeforeEndDateException

import handling.left as left
import handling.today as today

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
            budget = float(arguments[1])
        except ValueError:
            bot.send_message(message.chat.id, Messages.ADD_ARGUMENT_ERROR)
            return
        except CategoryAlreadyExistsException:
            bot.send_message(message.chat.id, Messages.CATEGORY_ALREADY_EXISTS.format(category))
    else:
        budget = 0

    bot.send_message(message.chat.id, Messages.ADD_CATEGORY_CREATED.format(category, budget))
    DatabaseService.add_category(message.chat.id, category, budget)

@bot.message_handler(commands=["change"])
def change_handler(message):
    command = message.text[8:]
    arguments = command.split(" ")
    try:
        category = arguments[0]
        money = float(arguments[1])
        DatabaseService.change_budget(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.CHANGE_SUCCESS.format(category, money))
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, Messages.CHANGE_ARGUMENT_ERROR)

@bot.message_handler(commands=["spend"])
def spend_handler(message):
    command = message.text[7:]
    arguments = command.split(" ")
    try:
        category = arguments[0]
        money = float(arguments[1])
        DatabaseService.add_transaction(message.chat.id, category, money)
        bot.send_message(message.chat.id, Messages.SPEND_SUCCESS.format(category, money))
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, Messages.SPEND_ARGUMENT_ERROR)

@bot.message_handler(commands=["left"])
def left_handler(message):
    categories = DatabaseService.get_categories(message.chat.id)
    result = left.get_fromatted_stats(categories)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=["setdates"])
def setdates_handler(message):
    command = message.text[10:]
    arguments = command.split(" ")
    try: 
        category = arguments[0]
        start = arguments[1]
        end = arguments[2]
        FORMAT = "%d.%m.%Y"
        startdate = datetime.datetime.strptime(start, FORMAT).date()
        enddate = datetime.datetime.strptime(end, FORMAT).date()

        DatabaseService.set_dates(message.chat.id, category, startdate, enddate)
        bot.send_message(message.chat.id, Messages.SET_DATES_SUCCESS)
    except NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except StartDaysNotBeforeEndDateException:
        bot.send_message(message.chat.id, Messages.SET_DATES_ORDER_ERROR)
    except Exception as e:
        bot.send_message(message.chat.id, Messages.SET_DATES_EXAMPLE)

@bot.message_handler(commands=["today"])
def today_handler(message):
    today.handle_today(message, bot)    


bot.infinity_polling()


import datetime

import database_service as database
from messages import Messages
from handling._args import extract_args

def handle_set_dates(message, bot):
    arguments = extract_args(message.text)
    
    try: 
        category = arguments[0]
        start = arguments[1]
        end = arguments[2]
        FORMAT = "%d.%m.%Y"
        startdate = datetime.datetime.strptime(start, FORMAT).date()
        enddate = datetime.datetime.strptime(end, FORMAT).date()

        database.set_dates(message.chat.id, category, startdate, enddate)
        bot.send_message(message.chat.id, Messages.SET_DATES_SUCCESS)
    except database.NoSuchCategoryExistsException:
        bot.send_message(message.chat.id, Messages.NO_SUCH_CATEGORY.format(category))
    except database.StartDaysNotBeforeEndDateException:
        bot.send_message(message.chat.id, Messages.SET_DATES_ORDER_ERROR)
    except Exception as e:
        bot.send_message(message.chat.id, Messages.SET_DATES_EXAMPLE)
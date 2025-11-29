from messages import Messages
from handling.statistics.model import StatisticsDTO


def view_statistics(bot, chat_id, category:str, stats:StatisticsDTO):
    """
    Function takes statistics (category and list of (WeekExpenseDTO, WeekStatisticsDTO),
    forms a message and send to the bot.
    """

    msg = ""

    msg += view_weeks_statistics(category, stats.week_statistics)
    msg += "\n\n"
    msg += view_per_day_statistics(stats.per_day_statistics)   

    bot.send_message(chat_id, msg, parse_mode="HTML")


def view_weeks_statistics(category, weeks_stats) -> str:
    msg = ""

    msg += Messages.STATS_HEADER.format(category)

    start_date = weeks_stats[0][0].start
    end_date = weeks_stats[-1][0].end
    msg += Messages.STATS_DATES.format(start_date, end_date)

    max_per_day = max([round(stat.total/stat.days,2) for (_, stat) in weeks_stats])

    for i, (week, stat) in enumerate(weeks_stats):

        total = round(stat.total, 2)
        per_day = round(stat.total/stat.days, 2)
        msg += Messages.STATS_WEEK.format(i+1, total, stat.days, per_day)

        if per_day == max_per_day:
            msg += Messages.STATS_MOST_PER_DAY
        
        msg += "\n\n"
    
    # Cutting the last \n\n
    msg = msg[:-2]
    return msg

def view_per_day_statistics(per_day_stats):

    msg = Messages.STATS_PER_DAY_HEADER

    day_names_strs = Messages.DAY_SHORT_NAMES.split(" ")
    for (day_name, stat) in zip(day_names_strs, per_day_stats):
        msg += f" - {day_name}: {round(stat, 2)}\n"

    return msg
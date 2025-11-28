

from messages import Messages


def view_statistics(bot, chat_id, category:str, weeks_stats):
    """
    Function takes statistics (category and list of (WeekExpenseDTO, WeekStatisticsDTO),
    forms a message and send to the bot.
    """

    msg = ""

    msg += Messages.STATS_HEADER.format(category)

    start_date = weeks_stats[0][0].week_start
    end_date = weeks_stats[-1][0].week_end
    msg += Messages.STATS_DATES.format(start_date, end_date)

    max_per_day = max([round(stat.total/stat.days,2) for (_, stat) in weeks_stats])

    for i, (week, stat) in enumerate(weeks_stats):

        total = round(stat.total, 2)
        per_day = round(stat.total/stat.days, 2)
        msg += Messages.STATS_WEEK.format(i+1, total, stat.days, per_day)

        if per_day == max_per_day:
            msg += Messages.STATS_MOST_PER_DAY
        
        msg += "\n\n"

    bot.send_message(chat_id, msg, parse_mode="HTML")
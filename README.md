# Intro
This is a Telegram bot for managing finances during trip, or just splitting the whole budget to categories.

# Motivation
This is a pet project, made to help me personally manage my finices. All business logic is dictated by every-day calculations I have been performing manualy.

# Running the bot
1. On your local machine create a new folder, navigate there and clone the repo.
```sh
mkdir TripFinanceBot
cd TripFinanceBot
git clone https://github.com/yaroslawliker/TripFinanceBot.git
```
2. Create your new bot at Telegram's official @BotFather and copy the token.
3. Create a file named `token.txt` in the root of the project and paste the token there.
4. Run the main.py file, for example from console `python3 main.py`.
5. Go to your bot's link you created at @BotFather and press 'Start'.

# Offinical instance
You can run your own instance of the bot as shown in the section above, or you can try to use the official (mine) instance:
@trip_finance_record_bot, but be aware: I am running it on a free hosting, so stops working regulary till I rerun it.

# Usage
Use `/start` command or button to begin the dialog with the bot. You can also use `/help` command.

Add a new category by using `/add` command, for example `/add food` or `/add hotel 300`, where 300 is budget.
You can change the budget of the category by using `/change`, e.g: `/change food 350`.

You can `/spend` some money in a category, e.g: `/spend food 7.5`.

You can then check how much is `/left` of every category.

You can add time limits to the categories with `/setdates`, e.g: `/setdates transfer 10.01.2025 17.02.2025`.
This will allow you to use commands:
* `/today` - see how much money have left for today (if we spread the whole amout to all days equally).
* `/week` - see how much money have left to the week.

# Technologies
This project uses [TelegramBotAPI](https://pytba.readthedocs.io/en/latest/index.html) and SQLite Database.

import datetime



class User:
    def __init__(self, chat_id:int):
        self.chat_id = chat_id

class Category:
    def __init__(self, id: int, 
                 name: str, budget: float, 
                 start_date: datetime.date, end_date: datetime.date, 
                 user_id: int):
        self.id = id
        self.name = name
        self.budget = budget
        self.start_date = start_date
        self.end_date = end_date
        self.chat_id = user_id


class Expense:
    def __init__(self, id: int, money: float, datetime: datetime.datetime, purpose: str, category_id: int):
        self.id = id
        self.money = money
        self.datetime = datetime
        self.purpose = purpose
        self.category_id = category_id

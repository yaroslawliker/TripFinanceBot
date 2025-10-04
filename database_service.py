import datetime

from entities import User, Category, Expense

from database.userDAO import UserDAO
from database.categoryDAO import CategoryDAO
from database.expenseDAO import ExpenseDAO


class CategoryAlreadyExistsException(KeyError):
    def __init__(self, user_id:int, category:str):
        self.user_id = user_id
        self.category = category
        super().__init__(f"Category {category} of user {user_id} already exists!")

class NoSuchCategoryExistsException(KeyError):
    def __init__(self, user_id:int, category:str):
        self.category = category
        self.user_id = user_id
        super().__init__(f"No such category {category} for user {user_id}")

class StartDaysNotBeforeEndDateException(ValueError):
    def __init__(self, startdate:datetime.date, enddate:datetime.date):
        self.startdate = startdate
        self.enddate = enddate
        super().__init__(f"Startdate {startdate} is not before enddate {enddate}")

###
### Common methods
###

class DatabaseService:

    def __init__(self, userDAO: UserDAO, categoryDAO: CategoryDAO, expenseDAO: ExpenseDAO):
        self._userDAO = userDAO
        self._categoryDAO = categoryDAO
        self._expenseDAO = expenseDAO

    def register_user(self, user_id:int):
        if self._userDAO.is_user_exists(user_id):
            raise RuntimeError(f"The user {user_id} is already registered")
        
        self._userDAO.add_user(User(user_id))

    def is_user_registered(self, user_id:int) -> bool:
        return self._userDAO.is_user_exists(user_id)
    
    def get_user(self, user_id:int) -> User:
        if not self._userDAO.is_user_exists(user_id):
            self.register_user(user_id)
        
        return User(user_id)
    
    def add_category(self, user_id:int, name:str, budget:float=0):
        if not self._userDAO.is_user_exists(user_id):
            raise RuntimeError(f"The user {user_id} is not registered")
        
        if not (self._categoryDAO.get_by_user_and_name(name, user_id) is None):
            raise CategoryAlreadyExistsException(user_id, name)
        
        self._categoryDAO.add(Category(None, name, budget, None, None, user_id))
    
    def change_budget(self, user_id:int, category_name:str, budget:float):

        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        category.budget = budget
        self._categoryDAO.update(category)
    
    def set_dates(self, user_id:int, category_name:str, startdate: datetime.date, enddate: datetime.date):

        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        if (startdate >= enddate):
            raise StartDaysNotBeforeEndDateException(startdate, enddate)
        
        category.start_date = startdate
        category.end_date = enddate
       
    def get_category(self, user_id:int, category_name:str) -> Category:
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        return category
    
    def get_categories(self, user_id:int) -> list:        
        return self._categoryDAO.get_all_by_user(user_id)
    


def add_transaction(user_id, category:str, money:float, dt:datetime.datetime=None):
    """Adds transaction (spending) to the given category"""
    user_data = get_user(user_id)

    assert isinstance(money, float)

    categories = user_data[CATEGORIES_KEY]

    if category not in categories:
        raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}")
    
    if (dt is None):
        dt = datetime.datetime.now()

    transaction = {
        MONEY_KEY:money,
        DATETIME_KEY:str(dt)
    }
    
    categories[category][TRANSACTIONS_KEY].append(transaction)

    save_user_data(user_id, user_data)

def get_categories(user_id):
    user_data = get_user(user_id)
    return user_data[CATEGORIES_KEY]

def get_dates(user_id, category:str):
    assert isinstance(category, str)

    user_data = get_user(user_id)

    categories = user_data[CATEGORIES_KEY]
    if category not in categories:
        raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}")
    
    # Checks if the time had been added
    if (STARTDATE_KEY not in categories[category]):
        return None
    
    startstr = categories[category][STARTDATE_KEY]
    endstr = categories[category][ENDDATE_KEY]

    startdate = datetime.datetime.strptime(startstr, DATE_FORMAT).date()
    enddate = datetime.datetime.strptime(endstr, DATE_FORMAT).date()
    
    return {
        STARTDATE_KEY: startdate,
        ENDDATE_KEY: enddate
    }
    
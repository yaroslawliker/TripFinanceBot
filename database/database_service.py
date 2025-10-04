import datetime

from functools import wraps

from entities import User, Category, Expense

from database.daos import UserDAO, CategoryDAO, ExpenseDAO

###
### Exception classes
###

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


### Database service class
class DatabaseService:

    def __init__(self, userDAO: UserDAO, categoryDAO: CategoryDAO, expenseDAO: ExpenseDAO):
        self._userDAO = userDAO
        self._categoryDAO = categoryDAO
        self._expenseDAO = expenseDAO


    ###
    ### User methods
    ### 
    
    def register_user(self, user_id:int):
        if self._userDAO.is_exists(user_id):
            raise RuntimeError(f"The user {user_id} is already registered")
        
        self._userDAO.add(User(user_id))

    def is_user_registered(self, user_id:int) -> bool:
        return self._userDAO.is_exists(user_id)
    
    def get_user(self, user_id:int) -> User:
        if not self._userDAO.is_exists(user_id):
            self.register_user(user_id)
        
        return User(user_id)
    
    def register_user_if_needed(func):
        """ Decorator to ensure that the user is registered before calling the function """
        @wraps(func)
        def wrapper(self, user_id:int, *args, **kwargs):
            if not self._userDAO.is_exists(user_id):
                self.register_user(user_id)
            return func(self, user_id, *args, **kwargs)
        return wrapper

    ###
    ### Category methods
    ###

    @register_user_if_needed
    def add_category(self, user_id:int, name:str, budget:float=0):
        
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
    

    ###
    ### Expense methods
    ###

    def add_expense(self, user_id:int, category_name:str, money:float, purpose:str):
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        dt = datetime.datetime.now()
        
        self._expenseDAO.add(Expense(None, money, dt, purpose, category.id))

    def get_expenses(self, user_id:int, category_name:str) -> list:
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        return self._expenseDAO.get_all_by_category(category.id)
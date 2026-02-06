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
    def __init__(self, user_id:int=None, category:str=None, id:int=None):
        self.category = category
        self.user_id = user_id
        self.id = id
        
        if id is not None:
            super().__init__(f"No such category with id {id}")
        else:
            super().__init__(f"No such category {category} for user {user_id}")

class StartDaysNotBeforeEndDateException(ValueError):
    def __init__(self, startdate:datetime.date, enddate:datetime.date):
        self.startdate = startdate
        self.enddate = enddate
        super().__init__(f"Startdate {startdate} is not before enddate {enddate}")

class ExpenseIsNotInTheCategory(Exception):
    pass

class ArchivatedIsAsUpdatedException(Exception):
    def __init__(self, archived:bool):
        self.archived = archived
        super().__init__(f"Category is already {'archivated' if archived else 'unarchivated'}")

class CategoryIsArchivedException(Exception):
    def __init__(self, category_name:str):
        self.category_name = category_name
        super().__init__(f"Category '{category_name}' is archived and cannot be used for this operation")



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
        
        self._categoryDAO.add(Category(None, name, budget, None, None, user_id, False))
    
    def change_budget(self, user_id:int, category_name:str, budget:float):

        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        if category.archived:
            raise CategoryIsArchivedException(category_name)
        
        category.budget = budget
        self._categoryDAO.update(category)
    
    def set_dates(self, user_id:int, category_name:str, startdate: datetime.date, enddate: datetime.date):

        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        if category.archived:
            raise CategoryIsArchivedException(category_name)
        
        if (startdate >= enddate):
            raise StartDaysNotBeforeEndDateException(startdate, enddate)
        
        category.start_date = startdate
        category.end_date = enddate

        self._categoryDAO.update(category)


    def _set_archived(self, user_id:int, category_name:str, archived:bool):
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        if (category.archived == archived):
            raise ArchivatedIsAsUpdatedException(archived)
        
        category.archived = archived
        self._categoryDAO.update(category)

    def archivate(self, user_id:int, category_name:str):
        """
        Archivates the category. 
        If the category is already archivated, raises ArchivatedIsAsUpdatedException.
        """
        self._set_archived(user_id, category_name, True)

    def unarchivate(self, user_id:int, category_name:str):
        """
        Unarchivates the category.
        If the category is already not archived, raises ArchivatedIsAsUpdatedException.
        """
        self._set_archived(user_id, category_name, False)

       
    def get_category(self, user_id:int, category_name:str) -> Category:
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        
        return category
    
    def get_categories(self, user_id:int, include_archived=False) -> list:        
        return self._categoryDAO.get_all_by_user(user_id, include_archived)
    
    def get_archived_categories(self, user_id:int) -> list:
        categoeis = self._categoryDAO.get_all_by_user(user_id, include_archived=True)
        return [category for category in categoeis if category.archived]
    

    ###
    ### Expense methods
    ###

    def add_expense(self, user_id:int, category_name:str, money:float, purpose:str):
        category = self._categoryDAO.get_by_user_and_name(category_name, user_id)
        if category is None:
            raise NoSuchCategoryExistsException(user_id, category_name)
        if category.archived:
            raise CategoryIsArchivedException(category_name)
        
        dt = datetime.datetime.now()
        
        self._expenseDAO.add(Expense(None, money, dt, purpose, category.id))

    def get_expenses(self, category_id:int) -> list:

        if self._categoryDAO.exists(category_id) is None:
            raise NoSuchCategoryExistsException(id=category_id)
        
        return self._expenseDAO.get_all_by_category(category_id)
    
    def delete_expense_if_in_category(self, expense_id, category_id):
        category = self._categoryDAO.get(category_id)
        if category is None:
            raise NoSuchCategoryExistsException(id=category_id)
        if category.archived:
            raise CategoryIsArchivedException(category.name)

        if not self._expenseDAO.exists_in_category(expense_id, category_id):
            raise ExpenseIsNotInTheCategory(f"No expense '{expense_id}' in categroy '{category_id}'")
        
        self._expenseDAO.delete(expense_id)

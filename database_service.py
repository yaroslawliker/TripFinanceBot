import datetime
from json_service import JSONService

class CategoryAlreadyExistsException(KeyError):
    pass

class NoSuchCategoryExistsException(KeyError):
    pass

class DatabaseService():

    # no-sql DB keys
    __CATEGORIES_KEY = "categories"
    __BUDGET_KEY = "budget"
    __TRANSACTIONS_KEY = "transactions"
    __MONEY_KEY = "money"
    __DATETIME_KEY = "datetime"


    ###
    ### Common methods
    ###

    def get_user_data_if_exists(user_id):
        user_id = str(user_id)
        database = JSONService.get_json()

        if user_id in database:
            return database[user_id]
        else:
            return None

    def save_user_data(user_id, user_data):
        database = JSONService.get_json()
        database[str(user_id)] = user_data
        JSONService.save_json(database)

    def register_user(user_id):
        
        user_data = DatabaseService.get_user_data_if_exists(user_id)
        if not (user_data is None):
            raise RuntimeError(f"The user {user_id} is already registered")
        userdata = {
            DatabaseService.__CATEGORIES_KEY : dict()
        }
        DatabaseService.save_user_data(user_id, userdata)

    def get_user(user_id:int):
        user_data = DatabaseService.get_user_data_if_exists(user_id)

        if user_data is None:
            DatabaseService.register_user(user_id)
            user_data = user_data = DatabaseService.get_user_data_if_exists(user_id)
        
        return user_data


    ###
    ### Use-case methods
    ###

    def add_category(user_id:int, category:str, budged:float = 0):
        """Adds category for the given user"""
        user_data = DatabaseService.get_user(user_id)
        
        categories = user_data[DatabaseService.__CATEGORIES_KEY]

        if category in categories:
            raise CategoryAlreadyExistsException(f"Category {category} of user {user_id} already exists!")
        
        categories[category] = {
            DatabaseService.__BUDGET_KEY: budged,
            DatabaseService.__TRANSACTIONS_KEY: []
        }

        DatabaseService.save_user_data(user_id, user_data)

    def change_budget(user_id:int, category:str, budget:float):
        """Sets the budget for the given category"""
        user_data = DatabaseService.get_user(user_id)

        categories = user_data[DatabaseService.__CATEGORIES_KEY]

        if category not in categories:
            raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}")
        
        categories[category][DatabaseService.__BUDGET_KEY] = budget

        DatabaseService.save_user_data(user_id, user_data)

    def add_transaction(user_id, category:str, money:float, dt:datetime.datetime=None):
        """Adds transaction (spending) to the given category"""
        user_data = DatabaseService.get_user(user_id)

        assert isinstance(money, float)

        categories = user_data[DatabaseService.__CATEGORIES_KEY]

        if category not in categories:
            raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}")
        
        if (dt is None):
            dt = datetime.datetime.now()

        transaction = {
            DatabaseService.__MONEY_KEY:money,
            DatabaseService.__DATETIME_KEY:str(dt)
        }
        
        categories[category][DatabaseService.__TRANSACTIONS_KEY].append(transaction)

        DatabaseService.save_user_data(user_id, user_data)




    
import datetime
from json_service import JSONService

class CategoryAlreadyExistsException(KeyError):
    pass

class NoSuchCategoryExistsException(KeyError):
    pass

class StartDaysNotBeforeEndDateException(ValueError):
    pass

# no-sql DB keys
CATEGORIES_KEY = "categories"
BUDGET_KEY = "budget"
TRANSACTIONS_KEY = "transactions"
MONEY_KEY = "money"
DATETIME_KEY = "datetime"
STARTDATE_KEY = "startdate"
ENDDATE_KEY = "enddate"

DATE_FORMAT = "%d.%m.%Y"

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
    
    user_data = get_user_data_if_exists(user_id)
    if not (user_data is None):
        raise RuntimeError(f"The user {user_id} is already registered")
    userdata = {
        CATEGORIES_KEY : dict()
    }
    save_user_data(user_id, userdata)

def get_user(user_id:int):
    user_data = get_user_data_if_exists(user_id)

    if user_data is None:
        register_user(user_id)
        user_data = user_data = get_user_data_if_exists(user_id)
    
    return user_data


###
### Use-case methods
###

def add_category(user_id:int, category:str, budged:float = 0):
    """Adds category for the given user"""
    user_data = get_user(user_id)
    
    categories = user_data[CATEGORIES_KEY]

    if category in categories:
        raise CategoryAlreadyExistsException(f"Category {category} of user {user_id} already exists!")
    
    categories[category] = {
        BUDGET_KEY: budged,
        TRANSACTIONS_KEY: []
    }

    save_user_data(user_id, user_data)

def change_budget(user_id:int, category:str, budget:float):
    """Sets the budget for the given category"""
    user_data = get_user(user_id)

    categories = user_data[CATEGORIES_KEY]

    if category not in categories:
        raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}")
    
    categories[category][BUDGET_KEY] = budget

    save_user_data(user_id, user_data)

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

def set_dates(user_id, category:str, startdate: datetime.date, enddate: datetime.date):
    assert isinstance(startdate, datetime.date) and isinstance(enddate, datetime.date) and isinstance(category, str)

    if (startdate >= enddate):
        raise StartDaysNotBeforeEndDateException(f"Startdate {enddate} is not after enddate {startdate}.")

    user_data = get_user(user_id)

    categories = user_data[CATEGORIES_KEY]
    if category not in categories:
        raise NoSuchCategoryExistsException(f"No category {category} for user {user_id}.")
    
    categories[category][STARTDATE_KEY] = startdate.strftime(DATE_FORMAT)
    categories[category][ENDDATE_KEY] = enddate.strftime(DATE_FORMAT)
    
    save_user_data(user_id, user_data)

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
    
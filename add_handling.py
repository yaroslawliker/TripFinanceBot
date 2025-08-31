from database_service import DatabaseService

def handle_add(user_id:int, arguments) -> str:
    category = arguments[0]
    if len(arguments) > 1:
        budget = arguments[1]
    else:
        budget = 0

    DatabaseService.add_category(user_id, category, budget)
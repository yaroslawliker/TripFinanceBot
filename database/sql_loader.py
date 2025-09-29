SQL_FILDER_PATH = "/database/tables/"

def load_sql_from_file(filename: str):
    filepath = SQL_FILDER_PATH + filename
    with open(filepath, "rt") as file:
        result = file.read()
    return result
        

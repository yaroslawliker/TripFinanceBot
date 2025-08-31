import json

class JSONService:

    JSON_FILE_NAME = "database.json"

    def get_json():
        with open(JSONService.JSON_FILE_NAME, "rt") as file:
            db = json.load(file)
        return db            

    def save_json(database):
        with open(JSONService.JSON_FILE_NAME, "wt") as file:
            json.dump(database, file, indent=2)

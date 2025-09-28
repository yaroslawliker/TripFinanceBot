import sqlite3

from entities import Category
from database.genericDAO import GenericDAO

class CategoryDAO(GenericDAO):

    def __category_from_row(row):
        
        id = row[0]
        name = row[1]
        budget = row[2]
        start_datetime = GenericDAO.datetime_to_str(row[3])
        end_datetime = GenericDAO.datetime_to_str(row[4])
        user_id = row[5]

        return Category(id, name, budget, start_datetime, end_datetime, user_id)

    def add_category(self, category: Category):
        self.__connection.execute(
            "INSERT INTO categories(name, budget, user_id) VALUES (?, ?, ?)", 
            (category.name, category.budget, category.user_id)
        )
    
    def update_category(self, category: Category):
        self.__connection.execute(
            "UPDATE categories SET name=?, budget=?, start_datetime=?, end_datetime=?, user_id=? WHERE id=?",
            (category.name, category.budget, category.start_dateime, category.end_datetime, category.user_id, category.id)
        )
    
    def get_category_by_user_and_name(self, name: str, chat_id:int):
        cursor = self.__connection.execute("SELECT * FROM categories WHERE (name = ? AND chat_id = ?)", (name, chat_id))
        row = cursor.fetchone()
        if row == None:
            return 
        else:
            return CategoryDAO.__category_from_row(row)
        
    
    def get_all_categories_of_user(self, chat_id:int) -> list:
        categories = []

        result = self.__connection.execute("SELECT * FROM categories WHERE chat_id = ?", (chat_id,)).fetchall()

        for row in result:
            categories.append(CategoryDAO.__category_from_row(row))

        return categories



    
    
    


    



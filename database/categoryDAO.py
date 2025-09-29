import sqlite3

from entities import Category
from database.genericDAO import GenericDAO

class CategoryDAO(GenericDAO):

    def _category_from_row(row):
        
        id = row[0]
        name = row[1]
        budget = row[2]
        start_date = GenericDAO.str_to_date(row[3])
        end_date = GenericDAO.str_to_date(row[4])
        user_id = row[5]

        return Category(id, name, budget, start_date, end_date, user_id)

    def add_category(self, category: Category):
        self._connection.execute(
            "INSERT INTO categories(name, budget, user_id) VALUES (?, ?, ?)", 
            (category.name, category.budget, category.user_id)
        )
    
    def update_category(self, category: Category):
        self._connection.execute(
            "UPDATE categories SET name=?, budget=?, start_datetime=?, end_datetime=?, user_id=? WHERE id=?",
            (category.name, category.budget, category.start_date, category.end_date, category.user_id, category.id)
        )
    
    def get_category_by_user_and_name(self, name: str, chat_id:int):
        cursor = self._connection.execute("SELECT * FROM categories WHERE (name = ? AND chat_id = ?)", (name, chat_id))
        row = cursor.fetchone()
        if row == None:
            return 
        else:
            return CategoryDAO._category_from_row(row)
        
    
    def get_all_categories_of_user(self, chat_id:int) -> list:
        categories = []

        result = self._connection.execute("SELECT * FROM categories WHERE chat_id = ?", (chat_id,)).fetchall()

        for row in result:
            categories.append(CategoryDAO._category_from_row(row))

        return categories



    
    
    


    



import sqlite3

from entities import Category
from database.daos.genericDAO import GenericDAO

class CategoryDAO(GenericDAO):

    def _from_row(row):
        """ Creates Category object from the given row from a database."""
        
        id = row[0]
        name = row[1]
        budget = row[2]
        start_date = GenericDAO.str_to_date(row[3])
        end_date = GenericDAO.str_to_date(row[4])
        user_id = row[5]

        return Category(id, name, budget, start_date, end_date, user_id)

    def add(self, category: Category):
        """
        Adds a new category from the given. 
        The id field is ignored, new id is stored in the database 
        """
        self._connection.execute(
            "INSERT INTO categories(name, budget, start_date, end_date, chat_id) VALUES (?, ?, ?, ?, ?)", 
            (category.name, category.budget, category.start_date, category.end_date, category.chat_id)
        )

    def exists(self, id):
        """ Returns True if category with given id exists. """
        cursor = self._connection.execute("SELECT * FROM categories WHERE id = ?", (id,))
        res = cursor.fetchall()
        return len(res) != 0
    
    def update(self, category: Category):
        """ Updates the given category using it's id"""
        self._connection.execute(
            "UPDATE categories SET name=?, budget=?, start_date=?, end_date=?, chat_id=? WHERE id=?",
            (
                category.name, category.budget, 
                GenericDAO.date_to_str(category.start_date), GenericDAO.date_to_str(category.end_date), 
                category.chat_id, category.id
            )
        )
    
    def get_by_user_and_name(self, name: str, chat_id:int):
        """ Reutrns Category of given name and user, or None if not found """
        cursor = self._connection.execute("SELECT * FROM categories WHERE (name = ? AND chat_id = ?)", (name, chat_id))
        row = cursor.fetchone()
        if row == None:
            return None
        else:
            return CategoryDAO._from_row(row)
        
    
    def get_all_by_user(self, chat_id:int) -> list:
        """ Returns all categories of given user"""
        categories = []

        result = self._connection.execute("SELECT * FROM categories WHERE chat_id = ?", (chat_id,)).fetchall()

        for row in result:
            categories.append(CategoryDAO._from_row(row))

        return categories



    
    
    


    



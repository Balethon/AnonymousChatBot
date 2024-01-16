from sqlite3 import connect

from user import User


class Database:
    connection = connect("database.db")

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"""
        cursor = cls.connection.cursor()
        cursor.execute(sql)
        cls.connection.commit()

    @classmethod
    def load_user(cls, user_id):
        sql = """"""
        return User()

    @classmethod
    def save_user(cls, user):
        pass

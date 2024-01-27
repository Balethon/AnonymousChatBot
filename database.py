from sqlite3 import connect

from user import User


class Database:
    connection = connect("database.db")

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, gender INTEGER, name TEXT, age INTEGER, match_id INTEGER)"""
        cursor = cls.connection.cursor()
        cursor.execute(sql)
        cls.connection.commit()

    @classmethod
    def insert_user(cls, user):
        sql = """INSERT INTO users VALUES (?, ?, ?, ?, ?)"""
        cursor = cls.connection.cursor()
        cursor.execute(sql, (user.id, user.gender, user.name, user.age, user.match_id))
        cls.connection.commit()

    @classmethod
    def update_user(cls, user):
        sql = """UPDATE users SET gender = ?, name = ?, age = ?, match_id = ? WHERE user_id = ?"""
        cursor = cls.connection.cursor()
        cursor.execute(sql, (user.gender, user.name, user.age, user.match_id, user.id))
        cls.connection.commit()

    @classmethod
    def save_user(cls, user):
        result = cls.select_user(user.id)
        if result is None:
            cls.insert_user(user)
        else:
            cls.update_user(user)

    @classmethod
    def select_user(cls, user_id):
        sql = """SELECT * FROM users WHERE user_id = ?"""
        cursor = cls.connection.cursor()
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()

    @classmethod
    def load_user(cls, user_id):
        result = cls.select_user(user_id)
        if result is None:
            return User(user_id)
        return User(*result)


Database.create_table()

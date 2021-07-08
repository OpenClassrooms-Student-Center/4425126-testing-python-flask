""" User Model """
import sqlite3 as sql
from config import dbname


class User:
    """User model class"""

    def create_table(self):
        """This function will create users table in database if it does not exists"""
        query = """CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL UNIQUE,
                    PASSWORD TEXT NOT NULL
                )"""
        try:
            with sql.connect(dbname) as conn:
                conn.execute(query)
        except:
            exit(4)

    def login(self, email, password):
        """Login user function or return None if fails"""
        query = "SELECT ID, Name FROM Users WHERE Email=? AND Password=?"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(
                    query,
                    (
                        email,
                        password,
                    ),
                )
                rows = list(cur.fetchall())
                if len(rows) == 1:
                    print(rows[0])
                    return rows[0]
                else:
                    return None
        except:
            conn.rollback()

        return None

    def register(self, name, email, password):
        """Register user or return None if fails"""
        query = "INSERT INTO Users(Name, Email, Password) VALUES(?, ?, ?)"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(
                    query,
                    (
                        name,
                        email,
                        password,
                    ),
                )
                conn.commit()
                return self.login(email, password)
        except:
            conn.rollback()
        return None

    def is_email_exists(self, email):
        """Check if email already exists or return None if not"""
        query = "SELECT ID, Name FROM Users WHERE Email=?"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(query, (email,))
                rows = list(cur.fetchall())
                if len(rows) == 1:
                    return rows[0]
                else:
                    return None
        except:
            conn.rollback()
        return None

    def clear(self):
        """This function will remove all records"""
        query = "DELETE FROM Users"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
        except:
            conn.rollback()


user = User()

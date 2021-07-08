""" Calculation table model """
import sqlite3 as sql
from config import dbname


class Calculation:
    """Calculation model class"""

    def create_table(self):
        """This function will create calculation table if it does not exist"""
        query = """CREATE TABLE IF NOT EXISTS Calculation (
                        ID INTEGER PRIMARY KEY,
                        Input_Value TEXT NOT NULL,
                        Input_Type INTEGER NOT NULL,
                        User_ID INTEGER NOT NULL,
                        FOREIGN KEY (User_ID)
                            REFERENCES Users(ID)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE
                    )"""
        try:
            with sql.connect(dbname) as conn:
                conn.execute(query)
        except:
            exit(4)

    def get_user_history(self, userID):
        """This function will load history of a user, recent 10 records only"""
        query = "SELECT Input_Value, Input_Type FROM Calculation WHERE User_ID=? ORDER BY User_ID DESC LIMIT 10"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(query, (userID,))
                rows = list(cur.fetchall())
                return rows
        except:
            conn.rollback()
        return None

    def add_calculation(self, userID, inp_value, inp_type):
        """This function will add calculation in database"""
        query = (
            "INSERT INTO Calculation(Input_Type, Input_Value, User_ID) VALUES(?, ?, ?)"
        )
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(
                    query,
                    (
                        inp_type,
                        inp_value,
                        userID,
                    ),
                )
                conn.commit()
                return 1
        except:
            conn.rollback()
        return None

    def clear(self):
        """This function will remove all records"""
        query = "DELETE FROM Calculation"
        try:
            with sql.connect(dbname) as conn:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
        except:
            conn.rollback()


calculation = Calculation()

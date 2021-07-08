""" for init_db function """
from .user import user
from .calculation import calculation


def init_db():
    """this function will create all tables in database"""
    user.create_table()
    calculation.create_table()


def clear_all():
    """this function will remove all records from tables in database"""
    calculation.clear()
    user.clear()

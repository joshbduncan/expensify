import sqlite3
from sqlite3 import Error

# import internal modules
import settings  # import project setting


db = settings.db


# connect to database
def connect():
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    return conn


# create new database it not installed
def create_db():
    sql_create_table = '''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        description	TEXT NOT NULL,
        card TEXT NOT NULL,
        vendor INTEGER NOT NULL,
        amount REAL NOT NULL,
        receipt TEXT NOT NULL,
        status INTEGER NOT NULL DEFAULT 0
    );'''

    execute(sql_create_table)


def execute(command, data=''):
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(command, data)
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# fetch all matching records
def fetchall(command, data=''):
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(command, data)
        fetch = c.fetchall()
        conn.commit()
        conn.close()
        return fetch
    except:
        conn.close()
        return False

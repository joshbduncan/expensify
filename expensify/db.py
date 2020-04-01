import os
import sqlite3
from sqlite3 import Error


############################
#### DATEBASE FUNCTIONS ####
############################


# set database name
db_file = 'expensify.db'
# get the path of the python program
program_path = os.path.dirname(os.path.realpath(__file__))
# set the correct path for the database
db_path = f'{program_path}/{db_file}'


# check for database, create if not there
def check_for_database():
    if os.path.exists(db_path):
        return True
    else:
        return False


# connect to database
def connect():
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)

    return conn


# create new database it not installed
def create_db():
    sql_create = '''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        description	TEXT NOT NULL,
        card TEXT NOT NULL,
        vendor INTEGER NOT NULL,
        amount REAL NOT NULL,
        receipt TEXT NOT NULL,
        status INTEGER NOT NULL DEFAULT 0
    );'''

    try:
        execute(sql_create)
    except Error as e:
        print(e)


# execute provided command and data in sql
def execute(command, data=''):
    try:
        conn = connect()
        c = conn.cursor()
        status = c.execute(command, data)
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# get a list of the table headers
def get_cols(table):
    try:
        conn = connect()
        c = conn.cursor()
        status = c.execute(f"SELECT * from {table}")
        cols = [item[0] for item in status.description]
        conn.commit()
        conn.close()
        return cols
    except:
        conn.close()
        return False


# fetch all matching records
def fetchall(command, data=''):
    try:
        conn = connect()
        c = conn.cursor()
        fetch = c.execute(command, data)
        data = [list(item) for item in fetch]
        cols = [item[0] for item in fetch.description]
        conn.commit()
        conn.close()

        # iterate through returned records and make dict with cols
        records = []
        for record in data:
            d = {}
            for i, col in enumerate(cols):
                d[col] = record[i]
            records.append(d)
        return records
    except:
        conn.close()
        return False

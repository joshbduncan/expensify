# import internal modules
import settings  # import project setting
import sqlite3


db = settings.db


# connect to database
def connect():
    conn = sqlite3.connect(db)
    return conn


# execute command to sqlite database and return status
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

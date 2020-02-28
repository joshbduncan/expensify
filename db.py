import sqlite3


def connect():
    conn = sqlite3.connect('expenses.db')
    return conn


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

import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    try:
        conn = sqlite3.connect('database/database.db')
        conn.row_factory = dict_factory
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

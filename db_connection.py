import sqlite3

from dotenv import load_dotenv
import os

load_dotenv()


def create_db_connection():
    # Create and return a database connection and cursor.
    try:
        connection = sqlite3.connect(os.getenv("DB_FILE_NAME"))
        if connection.cursor():
            print("Connected to SQLite Database")
        return connection
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def create_db_tables():
    with create_db_connection() as connection:
        cursor = connection.cursor()
        try:
            create_customers_table = '''
                CREATE TABLE IF NOT EXISTS Customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    balance REAL NOT NULL
                );
                '''
            cursor.execute("BEGIN;")
            cursor.execute(create_customers_table)
            connection.commit()
            print(f"Datatable created")

        except sqlite3.Error as e:
            connection.rollback()
            print(f"Database connection error: {e}")
            return None


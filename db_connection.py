import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def create_db_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL Database")
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

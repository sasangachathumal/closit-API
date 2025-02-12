import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    sql_script = f.read()
    print(sql_script)  # Debug: Print the SQL script
    connection.executescript(sql_script)

connection.commit()
connection.close()

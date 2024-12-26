from db_connection import create_db_connection


def get_items():
    """Fetch all items from the database."""
    connection = create_db_connection()
    if not connection:
        return {"error": "Failed to connect to the database"}, 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")  # Adjust "items" to your table name
        result = cursor.fetchall()
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def add_item(data):
    """Insert a new item into the database."""
    connection = create_db_connection()
    if not connection:
        return {"error": "Failed to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO items (name, description) VALUES (%s, %s)"  # Adjust columns
        cursor.execute(query, (data["name"], data["description"]))
        connection.commit()
        return {"message": "Item added successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



"""
Test the MySQL database connection.
"""

from db import get_db_connection


connection = None
cursor = None

try:

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")

    database = cursor.fetchone()

    print("Successfully connected to MySQL!")
    print("Database:", database[0])

    cursor.execute("SELECT COUNT(*) FROM products")

    total_products = cursor.fetchone()[0]

    print("Total products:", total_products)

except Exception as error:

    print("Database connection failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None:
        connection.close()
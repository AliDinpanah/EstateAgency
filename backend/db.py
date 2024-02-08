import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(query, args=None):
    cursor = connection.cursor(buffered=True)
    cursor.execute(query, args)
    connection.commit()
    print("Query executed successfully")
    return cursor

def executemany(query, args=None):
    cursor = connection.cursor(buffered=True)
    result = cursor.executemany(query, args)
    print(result)
    connection.commit()
    print("Query executed successfully")
    return cursor


def fetch_one(query, args=None):
    cursor = connection.cursor(buffered=True)
    cursor.execute(query, args)
    return cursor.fetchone()

def fetch_all(query, args=None):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query, args)
        return cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")


host = "127.0.0.1"
user = "root"
password = "1234"
database = "db"

connection = create_connection(host, user, password, database)
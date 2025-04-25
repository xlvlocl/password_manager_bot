import os
import sqlite3


def connect():
    db_name = (os.path.join("db", "passwords.db"))
    if db_name:
        connection = sqlite3.connect(db_name, check_same_thread=False)
        return connection.cursor(), connection
    return None


def disconnect(connection):
    connection.close()

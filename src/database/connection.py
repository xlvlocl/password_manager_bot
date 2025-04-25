import os
import sqlite3

# from src.config.settings import ADMIN_IDS


def connect(user_id: int):
    # you can add here check of id and choice of 2nd database, for example - to your girlfirend / boyfriend

    db_name = (os.path.join("db", "passwords.db"))
    if db_name:
        connection = sqlite3.connect(db_name, check_same_thread=False)
        return connection.cursor(), connection
    return None


def disconnect(connection):
    connection.close()

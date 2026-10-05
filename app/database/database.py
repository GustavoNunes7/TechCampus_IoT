import sqlite3
from flask import current_app

def get_db():
    connection = sqlite3.connect(current_app.config["DATABASE_PATH"])
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    connection = sqlite3.connect(current_app.config["DATABASE_PATH"])
    connection.execute("PRAGMA foreign_keys = ON")
    with open("app/database/schema.sql", "r", encoding="utf-8") as file:
        connection.executescript(file.read())
    connection.commit()
    connection.close()

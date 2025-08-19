import os
import sqlite3
import json

__all__ = [
    "initialize_db",
    "SeedData",
    "DBUtils"
]

DATABASE_FILE_NAME = "database.db"
PROCESS_FIELD_DB_NAME = "process"
MESSAGE_FIELD_DB_NAME = "messages"

def initialize_db():
    try:
        os.remove(DATABASE_FILE_NAME)
    except:...

    with sqlite3.connect(DATABASE_FILE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            name TEXT PRIMARY KEY,
            value TEXT
        );            
        """)
        conn.commit()

class SeedData:
    
    @staticmethod
    def seed_process_flag():
        with sqlite3.connect(DATABASE_FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", (PROCESS_FIELD_DB_NAME, 'false'))

    @staticmethod
    def seed_message(messages: dict):
        json_data = json.dumps(messages)
        with sqlite3.connect(DATABASE_FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", (MESSAGE_FIELD_DB_NAME, json_data))

class DBUtils:

    @staticmethod
    def switch_process_flag(value):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE data SET value=? WHERE name='{PROCESS_FIELD_DB_NAME}'", (f'{str(value).lower()}',))

    @staticmethod
    def get_process_flag():
        result = None
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT value FROM data WHERE name='{PROCESS_FIELD_DB_NAME}';")
            row = cursor.fetchone()
            if row and len(row) > 0:
                value = row[0]
                result = value.lower() in ('true', '1')
        return result

    @staticmethod
    def get_messages():
        result = None
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT value FROM data WHERE name='{MESSAGE_FIELD_DB_NAME}'")
            row = cursor.fetchone()
            if row and len(row) > 0:
                result = row[0]
        return json.loads(result)
    
    @staticmethod
    def set_messages(value):
        json_data = json.dumps(value)
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE data SET value=? WHERE name='{MESSAGE_FIELD_DB_NAME}'", (json_data,))
    
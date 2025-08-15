import sqlite3

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll_number INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

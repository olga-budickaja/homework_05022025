import sqlite3

from datetime import datetime


connection = sqlite3.connect("logs.sqlite3", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    status TEXT,
    lib VARCHAR(255) NOT NULL,
    execution_time REAL,
    timestamp VARCHAR(255) NOT NULL
)
""")
connection.commit()

def log_to_db(url, status, lib, execution_time):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (url, status, lib, execution_time, timestamp) VALUES (?, ?, ?, ?, ?)", (url, status, lib, execution_time, timestamp))
    connection.commit()

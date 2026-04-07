import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "lab.db")

schema = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
"""

seed = [
    ("alice", "alice123", "user"),
    ("bob", "bob123", "user"),
    ("admin", "supersecret", "admin"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript(schema)
cur.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", seed)
conn.commit()
conn.close()

print(f"Database initialized at {DB_PATH}")

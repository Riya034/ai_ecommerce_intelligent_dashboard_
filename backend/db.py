import sqlite3

# connect DB
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT,
    password TEXT
)
""")

conn.commit()

# add user
def add_user(email, password):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (email, password))
    conn.commit()

# ✅ THIS IS WHAT YOU ARE MISSING
def get_user(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone()

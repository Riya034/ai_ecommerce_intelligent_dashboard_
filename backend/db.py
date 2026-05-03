import sqlite3
from datetime import datetime

# connect DB
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")

# ---------------- OTP TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS otp (
    email TEXT PRIMARY KEY,
    otp TEXT,
    expires_at TEXT
)
""")

conn.commit()


# ---------------- USER FUNCTIONS ----------------
def add_user(email, password):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (email, password))
    conn.commit()


def get_user(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone()


# ---------------- OTP FUNCTIONS ----------------
def save_otp(email, otp, expires_at):
    cursor.execute("""
    INSERT OR REPLACE INTO otp (email, otp, expires_at)
    VALUES (?, ?, ?)
    """, (email, otp, expires_at))
    conn.commit()


def get_otp(email):
    cursor.execute("SELECT otp, expires_at FROM otp WHERE email=?", (email,))
    return cursor.fetchone()

def delete_otp(email):
    cursor.execute("DELETE FROM otp WHERE email=?", (email,))
    conn.commit()

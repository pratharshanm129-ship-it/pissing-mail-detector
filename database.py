"""
database.py
------------
Handles the SQLite database connection and initialization for the
AI Phishing Email Detector application.
"""

import sqlite3
import os

# Path to the SQLite database file (stored inside the "database" folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "phishing_detector.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")


def get_db_connection():
    """
    Creates and returns a new SQLite database connection.
    Rows are returned as dictionary-like objects so we can
    access columns by name (e.g. row["username"]).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initializes the database using the schema.sql script.
    This creates the 'users' and 'predictions' tables if they
    do not already exist. Safe to run multiple times because
    schema.sql drops tables before recreating them ONLY the
    first time app.py decides to call it (see app.py logic).
    """
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)

    conn = get_db_connection()
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database initialized successfully at:", DB_PATH)


def database_exists():
    """Returns True if the database file already exists on disk."""
    return os.path.exists(DB_PATH)

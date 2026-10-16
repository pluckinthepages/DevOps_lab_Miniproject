"""Create the CampusFind schema in the database named by DATABASE_URL.

Usage: python database/init_db.py
"""
import os
import sqlite3
import sys

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def db_path_from_url(url):
    """Turn 'sqlite:///file.db' or 'sqlite:////abs/file.db' into a sqlite3 path."""
    if not url.startswith("sqlite:///"):
        raise ValueError(f"Unsupported DATABASE_URL (only sqlite:/// is supported): {url}")
    path = url[len("sqlite:///"):]
    return path or ":memory:"


def connect(path):
    if path != ":memory:":
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


if __name__ == "__main__":
    url = os.environ.get("DATABASE_URL", "sqlite:///campusfind.db")
    path = db_path_from_url(url)
    conn = connect(path)
    init_db(conn)
    conn.close()
    print(f"Database initialised at {path}")
    sys.exit(0)

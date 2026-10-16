"""Seed CampusFind with a demo user and realistic lost & found records.

Usage: python scripts/seed_demo_data.py [--reset]
Uses DATABASE_URL (default sqlite:///campusfind.db). Safe to re-run: items are
only inserted when the demo user has none, unless --reset is given.
"""
import argparse
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash  # noqa: E402

from database.init_db import connect, db_path_from_url, init_db  # noqa: E402

DEMO_USERS = [
    ("demo", "demo@campus.edu", "DemoPassword123!"),
    ("priya.s", "priya@campus.edu", "DemoPassword123!"),
]

# (owner index, title, description, category, type, location, days ago, status, image_url)
ITEMS = [
    (0, "Blue Hydro Flask in Library 2nd Floor",
     "32oz navy blue Hydro Flask with a NASA sticker and a small dent near the base. Left on the long study table by the windows.",
     "accessories", "lost", "Central Library, 2nd floor study area", 1, "open", None),
    (1, "Sony WH-1000XM4 Headphones near Cafeteria",
     "Black Sony noise-cancelling headphones in a grey carry case. Found on a bench outside the main cafeteria around lunchtime.",
     "electronics", "found", "Main Cafeteria entrance benches", 2, "open", None),
    (0, "TI-84 Plus Calculator in Room 302",
     "Silver TI-84 Plus graphing calculator, name scratched off the back. Probably left after the Tuesday calculus exam.",
     "electronics", "lost", "Academic Block B, Room 302", 3, "claimed", None),
    (1, "Dorm Room Keys on Red Lanyard",
     "Two silver keys and a small fob on a red university lanyard. Found near the bike racks by Hostel 4.",
     "keys", "found", "Hostel 4 bike racks", 4, "resolved", None),
    (0, "Black Jansport Backpack",
     "Black Jansport backpack containing a Data Structures textbook and a pencil case. Has a keychain shaped like a cat.",
     "bags", "lost", "Sports Complex locker room", 5, "open", None),
    (1, "Grey University Hoodie",
     "Grey zip-up hoodie, size M, with the university crest on the chest. Left on a chair in the auditorium after the seminar.",
     "clothing", "found", "Main Auditorium, row F", 6, "open", None),
    (0, "Casio Wristwatch with Leather Strap",
     "Analog Casio watch with a brown leather strap. Sentimental value - a gift from my grandfather. Reward offered.",
     "accessories", "lost", "Basketball court, near the east bleachers", 8, "open", None),
    (1, "Set of Engineering Drawing Instruments",
     "Blue plastic case with compass, protractor, set squares and mechanical pencils. Found under a desk in the drawing hall.",
     "stationery", "found", "Engineering Drawing Hall", 9, "claimed", None),
    (0, "Apple AirPods Pro (Right Earbud Only)",
     "Lost the right AirPods Pro earbud somewhere between the parking lot and the CS department. White with no case.",
     "electronics", "lost", "Parking Lot to CS Department walkway", 10, "open", None),
    (1, "Student ID Card - Rohan M.",
     "University student ID card for Rohan M., Computer Engineering. Found on the floor at the photocopy shop.",
     "other", "found", "Campus photocopy & print shop", 12, "resolved", None),
    (0, "Green Spiral Notebook with Lab Notes",
     "A5 green spiral notebook full of chemistry lab notes for this semester. Name on the inside cover. Really need it back before finals!",
     "stationery", "lost", "Chemistry Lab 1", 14, "open", None),
    (1, "Silver Bike Lock Key",
     "Small silver Kryptonite key on a plain steel ring. Found in the grass next to the library bike stand.",
     "keys", "found", "Library bike stand", 15, "open", None),
]


def seed(conn, reset=False):
    init_db(conn)
    if reset:
        conn.execute("DELETE FROM items")
        conn.execute("DELETE FROM users WHERE email IN (?, ?)", tuple(u[1] for u in DEMO_USERS))
    user_ids = []
    for username, email, password in DEMO_USERS:
        row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            cur = conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            user_ids.append(cur.lastrowid)
        else:
            user_ids.append(row["id"])

    existing = conn.execute("SELECT COUNT(*) FROM items WHERE user_id IN (?, ?)", tuple(user_ids)).fetchone()[0]
    if existing:
        conn.commit()
        return 0

    today = date.today()
    # Insert oldest first so the newest record shows first on the board.
    for owner, title, desc, cat, kind, loc, days, status, img in sorted(ITEMS, key=lambda i: -i[6]):
        conn.execute(
            "INSERT INTO items (user_id, title, description, category, item_type, location, item_date, "
            "image_url, contact_email, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', ?))",
            (user_ids[owner], title, desc, cat, kind, loc, (today - timedelta(days=days)).isoformat(),
             img, DEMO_USERS[owner][1], status, f"-{days} days"),
        )
    conn.commit()
    return len(ITEMS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reset", action="store_true", help="delete all items and re-seed")
    args = parser.parse_args()
    path = db_path_from_url(os.environ.get("DATABASE_URL", "sqlite:///campusfind.db"))
    conn = connect(path)
    added = seed(conn, reset=args.reset)
    conn.close()
    print(f"Seeded {added} items into {path}." if added else f"Demo data already present in {path}; nothing added.")
    print("Demo login: demo@campus.edu / DemoPassword123!")

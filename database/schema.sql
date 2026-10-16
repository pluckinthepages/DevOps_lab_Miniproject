-- CampusFind schema (SQLite). Idempotent: safe to run on every start.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title         TEXT NOT NULL CHECK (length(title) BETWEEN 3 AND 100),
    description   TEXT NOT NULL CHECK (length(description) BETWEEN 10 AND 1000),
    category      TEXT NOT NULL CHECK (category IN ('electronics', 'bags', 'stationery', 'clothing', 'keys', 'accessories', 'other')),
    item_type     TEXT NOT NULL CHECK (item_type IN ('lost', 'found')),
    location      TEXT NOT NULL,
    item_date     DATE NOT NULL,
    image_url     TEXT NULL,
    contact_email TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'claimed', 'resolved')),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_items_user ON items(user_id);
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);

import os
import sys
import tempfile

import pytest

# Point the module-level app at a throwaway DB before app.py is imported,
# so the test run never creates or touches campusfind.db.
_IMPORT_DB = os.path.join(tempfile.mkdtemp(), "import.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_IMPORT_DB}"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, get_db  # noqa: E402

PASSWORD = "Password123!"


@pytest.fixture
def app(tmp_path):
    app = create_app("testing", {"DATABASE_URL": f"sqlite:///{tmp_path / 'test.db'}"})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        yield get_db()


def register(client, username, email, password=PASSWORD):
    return client.post("/register", data={
        "username": username, "email": email,
        "password": password, "confirm_password": password,
    })


def login(client, email, password=PASSWORD):
    return client.post("/login", data={"email": email, "password": password})


def valid_item(**overrides):
    data = {
        "title": "Blue Hydro Flask",
        "description": "Navy blue bottle with a NASA sticker on it.",
        "category": "accessories",
        "item_type": "lost",
        "location": "Library 2nd floor",
        "item_date": "2024-01-15",
        "contact_email": "owner@campus.edu",
        "image_url": "",
    }
    data.update(overrides)
    return data


@pytest.fixture
def auth_client(client):
    register(client, "alice", "alice@campus.edu")
    return client


@pytest.fixture
def second_client(app):
    other = app.test_client()
    register(other, "bob", "bob@campus.edu")
    return other


@pytest.fixture
def make_item(auth_client, app):
    def _make(**overrides):
        auth_client.post("/items/new", data=valid_item(**overrides))
        with app.app_context():
            return get_db().execute("SELECT MAX(id) FROM items").fetchone()[0]
    return _make

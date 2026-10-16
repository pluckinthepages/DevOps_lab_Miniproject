from tests.conftest import valid_item


def count(db):
    return db.execute("SELECT COUNT(*) FROM items").fetchone()[0]


def test_missing_required_fields(auth_client, db):
    resp = auth_client.post("/items/new", data={"title": "", "description": ""})
    assert resp.status_code == 400
    html = resp.get_data(as_text=True)
    assert "Title must be between 3 and 100 characters." in html
    assert "Description must be between 10 and 1000 characters." in html
    assert count(db) == 0


def test_field_length_boundaries(auth_client, db):
    assert auth_client.post("/items/new", data=valid_item(title="ab")).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(title="x" * 101)).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(description="short")).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(description="x" * 1001)).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(contact_email="not-an-email")).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(item_date="2999-01-01")).status_code == 400
    assert auth_client.post("/items/new", data=valid_item(image_url="javascript:alert(1)")).status_code == 400
    assert count(db) == 0
    assert auth_client.post("/items/new", data=valid_item(title="abc", description="x" * 10)).status_code == 302
    assert count(db) == 1


def test_invalid_item_type(auth_client, db):
    resp = auth_client.post("/items/new", data=valid_item(item_type="stolen"))
    assert resp.status_code == 400
    assert b"Item type must be" in resp.data
    assert count(db) == 0


def test_invalid_category(auth_client, db):
    resp = auth_client.post("/items/new", data=valid_item(category="weapons"))
    assert resp.status_code == 400
    assert b"valid category" in resp.data
    assert count(db) == 0


def test_invalid_status_rejected(auth_client, make_item, db):
    item_id = make_item()
    auth_client.post(f"/items/{item_id}/status", data={"status": "deleted"})
    assert db.execute("SELECT status FROM items WHERE id = ?", (item_id,)).fetchone()[0] == "open"


def test_sql_injection_resilience(auth_client, make_item, client, db):
    make_item(title="Visible Item")
    payload = "' OR '1'='1"
    # Search: payload treated as literal text, so nothing matches
    html = client.get("/", query_string={"q": payload}).get_data(as_text=True)
    assert "No matching items" in html
    assert "Visible Item" not in html
    # Destructive payload in filters is ignored, table survives
    client.get("/", query_string={"category": "x'; DROP TABLE items; --"})
    assert count(db) == 1
    # Stored as plain text, and auto-escaped on render
    auth_client.post("/items/new", data=valid_item(title=payload, description="<script>alert(1)</script> desc"))
    row = db.execute("SELECT id, title FROM items WHERE title = ?", (payload,)).fetchone()
    assert row["title"] == payload
    detail = client.get(f"/items/{row['id']}").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in detail
    assert "&lt;script&gt;" in detail
    # Login bypass attempt fails
    resp = client.post("/login", data={"email": payload, "password": payload})
    assert resp.status_code == 401


def test_search_and_filtering(client, make_item, auth_client):
    make_item(title="Sony Headphones", category="electronics", item_type="found")
    make_item(title="Red Lanyard Keys", category="keys", item_type="lost",
              description="Two dorm keys on a red lanyard.")
    resolved = make_item(title="Grey Hoodie", category="clothing", item_type="found")
    auth_client.post(f"/items/{resolved}/status", data={"status": "resolved"})

    html = client.get("/?q=headphones").get_data(as_text=True)
    assert "Sony Headphones" in html and "Red Lanyard Keys" not in html

    html = client.get("/?q=dorm").get_data(as_text=True)  # matches description
    assert "Red Lanyard Keys" in html and "Sony Headphones" not in html

    html = client.get("/?category=keys").get_data(as_text=True)
    assert "Red Lanyard Keys" in html and "Grey Hoodie" not in html

    html = client.get("/?status=resolved").get_data(as_text=True)
    assert "Grey Hoodie" in html and "Sony Headphones" not in html

    html = client.get("/?type=found&status=open").get_data(as_text=True)
    assert "Sony Headphones" in html and "Grey Hoodie" not in html and "Red Lanyard Keys" not in html
    assert 'value="found" selected' in html  # filter state retained


def test_register_validation(client, db):
    resp = client.post("/register", data={"username": "a", "email": "bad", "password": "x", "confirm_password": "y"})
    assert resp.status_code == 400
    client.post("/register", data={"username": "dave", "email": "dave@campus.edu",
                                   "password": "Password123!", "confirm_password": "Password123!"})
    dup = client.post("/register", data={"username": "dave", "email": "dave@campus.edu",
                                         "password": "Password123!", "confirm_password": "Password123!"})
    assert dup.status_code == 400
    row = db.execute("SELECT password_hash FROM users WHERE username = 'dave'").fetchone()
    assert row["password_hash"] != "Password123!"

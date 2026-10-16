from tests.conftest import valid_item


def test_create_item_authenticated(auth_client, db):
    resp = auth_client.post("/items/new", data=valid_item(title="Lost Calculator"))
    assert resp.status_code == 302
    assert "/items/" in resp.headers["Location"]
    row = db.execute("SELECT * FROM items WHERE title = ?", ("Lost Calculator",)).fetchone()
    assert row is not None
    assert row["status"] == "open"
    assert row["item_type"] == "lost"


def test_create_item_unauthenticated(client, db):
    resp = client.get("/items/new")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
    resp = client.post("/items/new", data=valid_item())
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
    assert db.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0


def test_item_detail_view(client, make_item):
    item_id = make_item(title="Sony Headphones", location="Cafeteria", item_type="found")
    html = client.get(f"/items/{item_id}").get_data(as_text=True)
    assert "Sony Headphones" in html
    assert "Cafeteria" in html
    assert "owner@campus.edu" in html
    assert "badge-found" in html
    assert "Manage your listing" in html


def test_item_detail_not_found(client):
    assert client.get("/items/9999").status_code == 404


def test_update_item_owner(auth_client, make_item, db):
    item_id = make_item()
    resp = auth_client.post(f"/items/{item_id}/edit", data=valid_item(
        title="Updated Title", description="An updated and longer description.", status="claimed"))
    assert resp.status_code == 302
    row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    assert row["title"] == "Updated Title"
    assert row["description"] == "An updated and longer description."
    assert row["status"] == "claimed"

    auth_client.post(f"/items/{item_id}/status", data={"status": "resolved"})
    assert db.execute("SELECT status FROM items WHERE id = ?", (item_id,)).fetchone()[0] == "resolved"


def test_unauthorized_edit_forbidden(make_item, second_client, db):
    item_id = make_item(title="Alice Item")
    assert second_client.get(f"/items/{item_id}/edit").status_code == 403
    assert second_client.post(f"/items/{item_id}/edit", data=valid_item(title="Hacked")).status_code == 403
    assert second_client.post(f"/items/{item_id}/status", data={"status": "resolved"}).status_code == 403
    assert second_client.post(f"/items/{item_id}/delete").status_code == 403
    row = db.execute("SELECT title, status FROM items WHERE id = ?", (item_id,)).fetchone()
    assert row["title"] == "Alice Item"
    assert row["status"] == "open"
    # Non-owners don't see owner controls
    assert "Manage your listing" not in second_client.get(f"/items/{item_id}").get_data(as_text=True)


def test_delete_item(auth_client, make_item, db):
    item_id = make_item()
    resp = auth_client.post(f"/items/{item_id}/delete")
    assert resp.status_code == 302
    assert db.execute("SELECT COUNT(*) FROM items WHERE id = ?", (item_id,)).fetchone()[0] == 0


def test_login_logout_flow(client):
    from tests.conftest import login, register
    register(client, "carol", "carol@campus.edu")
    client.get("/logout")
    assert client.get("/items/new").status_code == 302
    assert login(client, "carol@campus.edu", "wrong-password").status_code == 401
    assert login(client, "carol@campus.edu").status_code == 302
    assert client.get("/items/new").status_code == 200

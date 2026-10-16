def test_home_page_status_code(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<title>CampusFind" in resp.data
    assert b"CampusFind" in resp.data


def test_dashboard_statistics(client, make_item):
    make_item(item_type="lost")
    make_item(item_type="lost")
    found_id = make_item(item_type="found")
    client.post(f"/items/{found_id}/status", data={"status": "resolved"})

    html = client.get("/").get_data(as_text=True)
    assert '<span class="stat-value" id="stat-total">3</span>' in html
    assert '<span class="stat-value" id="stat-lost">2</span>' in html
    assert '<span class="stat-value" id="stat-found">1</span>' in html
    assert '<span class="stat-value" id="stat-resolved">1</span>' in html


def test_empty_database_render(client):
    html = client.get("/").get_data(as_text=True)
    assert "No items reported yet" in html
    assert '<span class="stat-value" id="stat-total">0</span>' in html
    assert 'class="card"' not in html


def test_pagination(client, make_item):
    for i in range(12):
        make_item(title=f"Item number {i:02d}")
    page1 = client.get("/").get_data(as_text=True)
    page2 = client.get("/?page=2").get_data(as_text=True)
    assert "Page 1 of 2" in page1
    assert page1.count('class="card"') == 9
    assert page2.count('class="card"') == 3

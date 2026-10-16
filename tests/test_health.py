import sqlite3

import app as app_module


def test_health_endpoint_healthy(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "healthy"
    assert body["database"] == "connected"
    assert body["version"] == "1.0.0"
    assert "timestamp" in body


def test_health_endpoint_db_failure(client, monkeypatch):
    def broken_db():
        raise sqlite3.OperationalError("unable to open database file")

    monkeypatch.setattr(app_module, "get_db", broken_db)
    resp = client.get("/health")
    assert resp.status_code == 503
    body = resp.get_json()
    assert body["status"] == "unhealthy"
    assert body["database"] == "disconnected"
    assert "unable to open database file" in body["error"]

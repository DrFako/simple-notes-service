from uuid import uuid4

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_crud_notes():
    # CREATE
    resp = client.post("/api/notes/", json={"title": "Test Note", "content": "Some content"})
    assert resp.status_code == 201
    note = resp.json()
    assert note["title"] == "Test Note"
    assert note["content"] == "Some content"
    assert "id" in note and "created_at" in note
    note_id = note["id"]

    # GET ALL
    resp = client.get("/api/notes/")
    assert resp.status_code == 200
    all_notes = resp.json()
    assert any(n["id"] == note_id for n in all_notes)

    # GET ONE
    resp = client.get(f"/api/notes/{note_id}")
    assert resp.status_code == 200
    fetched = resp.json()
    assert fetched["title"] == "Test Note"

    # UPDATE
    resp = client.put(f"/api/notes/{note_id}", json={"title": "Updated!"})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["title"] == "Updated!"

    # BAD UPDATE (empty title)
    resp = client.put(f"/api/notes/{note_id}", json={"title": ""})
    assert resp.status_code == 400

    # DELETE
    resp = client.delete(f"/api/notes/{note_id}")
    assert resp.status_code == 204

    # DELETE AGAIN (not found)
    resp = client.delete(f"/api/notes/{note_id}")
    assert resp.status_code == 404

    # GET unknown
    random_id = str(uuid4())
    resp = client.get(f"/api/notes/{random_id}")
    assert resp.status_code == 404

    # CREATE invalid (missing title)
    resp = client.post("/api/notes/", json={"content": "No title"})
    assert resp.status_code == 400 or resp.status_code == 422

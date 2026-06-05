from fastapi.testclient import TestClient
from hello import app
client = TestClient(app)

def test_create_mood():
    response = client.post("/mood", json={
        "date": "2026-06-02",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!"
    })
    assert response.status_code == 200
    assert response.json() == {
        "date": "2026-06-02",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!"
    }

def test_get_mood_by_date():
    response = client.get("/mood/2026-06-02")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2026-06-02",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!"
    }

def test_get_all_moods():
    response = client.get("/mood")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_delete_mood():
    response = client.delete("/mood/2026-06-02")
    assert response.status_code == 200
    assert response.json() == {"message": "Mood entry deleted successfully."}


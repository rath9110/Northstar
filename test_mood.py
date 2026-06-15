from fastapi.testclient import TestClient
from hello import app
from weather import get_weather_code_for_today, dict_weather_codes
client = TestClient(app)


def test_weather_code_for_today():
    weather_code = get_weather_code_for_today()
    assert weather_code in [
        'clear', 'mostly-clear', 'partly-cloudy', 'overcast', 'fog', 'rime-fog',
        'light-drizzle', 'moderate-drizzle', 'dense-drizzle', 'light-rain',
        'moderate-rain', 'heavy-rain', 'light-freezing-drizzle',
        'dense-freezing-drizzle', 'light-freezing-rain', 'heavy-freezing-rain',
        'snow-grains', 'snow-showers', 'snow-showers-heavily',
        'slight-snowfall', 'moderate-snowfall', 'heavy-snowfall',
        'thunderstorm', 'thunderstorm-with-hail'
    ]

def test_create_mood():
    response = client.post("/mood", json={
        "date": "2999-12-31",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!",
        "weather_code": "clear"
    })
    assert response.status_code == 200
    body = response.json()
    expected = {
        "date": "2999-12-31",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!"
    }
    assert expected.items() <= body.items()
    assert body["weather_code"] in dict_weather_codes.values()


def test_get_mood_by_date():
    response = client.get("/mood/2999-12-31")
    assert response.status_code == 200
    body = response.json()
    expected = {
        "date": "2999-12-31",
        "happiness": 8,
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!",
    }
    assert expected.items() <= body.items()
    assert body["weather_code"] in dict_weather_codes.values()

def test_get_all_moods():
    response = client.get("/mood")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        assert len(response.json()) > 0
    else:
        assert response.json() == []

def test_delete_mood():
    response = client.delete("/mood/2999-12-31")
    assert response.status_code == 200
    assert response.json() == {"message": "Mood entry deleted successfully."}

def test_post_invalid_energy():
    response = client.post("/mood", json={
        "date": "2999-12-31",
        "happiness": 8,
        "energy": 15,  # Invalid energy value
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!",
        "weather_code": "clear"
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_post_invalid_happiness():
    response = client.post("/mood", json={
        "date": "2999-12-31",
        "happiness": 15,  # Invalid happiness value
        "energy": 7,
        "stressed": False,
        "friends_family_time": True,
        "notes": "Had a good day!",
        "weather_code": "clear"
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_get_nonexistent_mood():
    response = client.get("/mood/1999-01-01")  # Assuming this date does not exist in the database
    assert response.status_code == 404
    assert response.json() == {"detail": "Mood entry not found for the given date."}


def health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
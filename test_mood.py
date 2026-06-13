from fastapi.testclient import TestClient
from hello import app
from weather import get_weather_code_for_today
client = TestClient(app)

dict_weather_codes = {
    0: 'clear',
    1: 'mostly-clear',
    2: 'partly-cloudy',
    3: 'overcast',
    45: 'fog',
    48: 'rime-fog',
    51: 'light-drizzle',
    53: 'moderate-drizzle',
    55: 'dense-drizzle',
    80: 'light-rain',
    81: 'moderate-rain',
    82: 'heavy-rain',
    61: 'light-rain',
    63: 'moderate-rain',
    65: 'heavy-rain',
    56: 'light-freezing-drizzle',
    57: 'dense-freezing-drizzle',
    66: 'light-freezing-rain',
    67: 'heavy-freezing-rain',
    77: 'snow-grains',
    85: 'snow-showers',
    86: 'snow-showers-heavily',
    71: 'slight-snowfall',
    73: 'moderate-snowfall',
    75: 'heavy-snowfall',
    95: 'thunderstorm',
    96: 'thunderstorm-with-hail',
    99: 'thunderstorm-with-hail'
}


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
    assert len(response.json()) > 0

def test_delete_mood():
    response = client.delete("/mood/2999-12-31")
    assert response.status_code == 200
    assert response.json() == {"message": "Mood entry deleted successfully."}


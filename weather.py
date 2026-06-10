import requests
import datetime

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

def get_weather_code_for_today(lat=59.334591, lon=18.063240):
    lat = lat
    lon = lon
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    url = f"https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": yesterday,
        "end_date": yesterday,
        "daily": ["weather_code"],
        "timezone": "auto"
    }

    openmeteo_response = requests.get(url, params=params)
        
    if openmeteo_response.status_code == 200:
        weather_data = openmeteo_response.json()
        weather_code = weather_data['daily']['weather_code'][0]
        return dict_weather_codes.get(weather_code, 'Unknown')

def __init__():
    print(get_weather_code_for_today())

__init__()


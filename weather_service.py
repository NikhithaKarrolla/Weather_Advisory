import requests
from config import OPENWEATHER_API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(lat: float, lon: float):

    url = f"{BASE_URL}/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Weather API error: {response.status_code} - {response.text}"
        )

    return response.json()


def get_forecast(lat: float, lon: float):

    url = f"{BASE_URL}/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Forecast API error: {response.status_code} - {response.text}"
        )

    return response.json()
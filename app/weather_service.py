import requests
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city: str) -> dict:
    """
    Fetch current weather for a given city.
    Returns a cleaned dictionary with the data we care about.
    """
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # raises an error if request failed

    data = response.json()

    # We clean and shape the data — don't just return the raw blob
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }
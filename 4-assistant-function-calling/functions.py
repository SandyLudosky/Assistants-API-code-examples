import openai
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Constants
API_KEY = os.getenv("OPENAI_API_KEY")  # Get the key from environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

client = openai.OpenAI()
openai.api_key = API_KEY


def kelvin_to_celsius(kelvin):
    return json.dumps(round(kelvin - 273.15))


def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9 / 5 + 32, 2)


def geo_code(location):
    loc = location.split(",")[0]
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={loc}&appid={WEATHER_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        coordinates = response.json()
        print(coordinates)
        lat = coordinates[0].get("lat")
        lon = coordinates[0].get("lon")
        return lat, lon

    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None, None


def get_current_weather(location, unit="celsius"):
    lat, lon = geo_code(location)

    if lat is None or lon is None:
        print("Failed to get location coordinates.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        current_temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]

        weather_info = {
            "location": location,
            "temperature": kelvin_to_celsius(current_temp)
            if unit == "celsius"
            else kelvin_to_fahrenheit(current_temp),
            "unit": unit,
            "forecast": description,
        }

        # make sure to convert to stringified json object
        return json.dumps(weather_info)

    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return

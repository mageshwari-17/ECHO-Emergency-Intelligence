
import requests
import os


def get_weather(location):

    api_key = os.getenv("OPENWEATHER_API_KEY")

    # If API key is not available
    if not api_key:
        return {
            "location": location,
            "temperature": "N/A",
            "condition": "Weather API key missing",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "error": "API key not configured"
        }

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        weather_info = {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "error": None
        }

        return weather_info

    except requests.exceptions.HTTPError as e:

        return {
            "location": location,
            "temperature": "N/A",
            "condition": "Weather API error",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "error": str(e)
        }

    except requests.exceptions.RequestException as e:

        return {
            "location": location,
            "temperature": "N/A",
            "condition": "Connection failed",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "error": str(e)
        }

    except (KeyError, IndexError, TypeError, ValueError) as e:

        return {
            "location": location,
            "temperature": "N/A",
            "condition": "Invalid weather data",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "error": str(e)
        }

import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from app import get_coordinates

def save_weather_overview_as_json(lat, lon, api_key, filename="wsummary.json"):
    """
    Fetches weather data, structures the key summary info, and saves it as a JSON file.
    """
    exclude_parts = "minutely,hourly,alerts"
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Structure the data into a Python dictionary

        # Today's data
        current_weather = data.get('current', {})
        today_data = data['daily'][0]
        today_overview = {
            "date": datetime.fromtimestamp(current_weather.get('dt')).strftime('%A, %d %B %Y'),
            "summary": today_data.get('summary', "No summary available."),
            "current_temp_celsius": current_weather.get('temp'),
            "feels_like_celsius": current_weather.get('feels_like'),
            "condition": current_weather.get('weather', [{}])[0].get('description', 'N/A').title()
        }

        # Tomorrow's data
        tomorrow_data = data['daily'][1]
        tomorrow_overview = {
            "date": datetime.fromtimestamp(tomorrow_data.get('dt')).strftime('%A, %d %B %Y'),
            "summary": tomorrow_data.get('summary', "No summary available."),
            "day_temp_celsius": tomorrow_data.get('temp', {}).get('day'),
            "night_temp_celsius": tomorrow_data.get('temp', {}).get('night'),
            "condition": tomorrow_data.get('weather', [{}])[0].get('description', 'N/A').title(),
            "chance_of_rain_percent": tomorrow_data.get('pop', 0) * 100
        }

        # Combine everything into a final dictionary
        structured_output = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "today": today_overview,
            "tomorrow": tomorrow_overview
        }

        # Save the dictionary to a JSON file
        with open(filename, 'w') as json_file:
            # indent=4 makes the JSON file readable
            json.dump(structured_output, json_file, indent=4)
        
        return f" Successfully saved weather overview to {filename}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"A network error occurred: {req_err}"
    except (KeyError, IndexError):
        return "Error: Could not parse the weather data from the API response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    
    if not api_key:
        print("Error: OPEN_WEATHER_API_KEY not found in .env file.")
    else:
        lat, lon = get_coordinates()
        result_message = save_weather_overview_as_json(lat, lon, api_key)
        print(result_message)

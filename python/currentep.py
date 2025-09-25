import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Assuming get_coordinates is in a file named app.py in the same directory.
# If it's not, you might need to adjust the import.
try:
    from app import get_coordinates
    lat, lon = get_coordinates()
except ImportError:
    print("Warning: 'app.py' not found. You'll need to provide coordinates manually.")
    # Define a dummy function if app.py is not available
    

def fetch_current_ep(lat, lon):
    """
    Fetches current weather data from OpenWeatherMap API for given coordinates.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        dict: A dictionary containing the weather data in JSON format, 
              or None if an error occurs.
    """
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    if not api_key:
        print("Error: OPEN_WEATHER_API_KEY not found in environment variables.")
        return None

    exclude_parts = "minutely,hourly,daily,alerts"
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        # Raises an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

def display_weather(data):
    """Prints formatted weather data from the JSON object."""
    if not data:
        print("No weather data to display.")
        return

    print("=" * 30)
    print("--- Detailed Current Weather ---")
    current_data = data.get('current', {})
    
    if not current_data:
        print("'current' data block is not available.")
        return

    # Time and Location
    dt_object = datetime.fromtimestamp(current_data.get('dt', 0))
    sunrise_obj = datetime.fromtimestamp(current_data.get('sunrise', 0))
    sunset_obj = datetime.fromtimestamp(current_data.get('sunset', 0))
    print(f"Time: {dt_object.strftime('%I:%M %p')}")
    print(f"Sunrise: {sunrise_obj.strftime('%I:%M %p')}")
    print(f"Sunset: {sunset_obj.strftime('%I:%M %p')}")
    print("-" * 20)

    # Weather Condition
    weather_info = current_data.get('weather', [{}])[0]
    print(f"Condition: {weather_info.get('description', 'N/A').title()}")
    print("-" * 20)

    # Main Metrics
    print(f"Temperature: {current_data.get('temp', 'N/A')}°C")
    print(f"Feels Like: {current_data.get('feels_like', 'N/A')}°C")
    print(f"Pressure: {current_data.get('pressure', 'N/A')} hPa")
    print(f"Humidity: {current_data.get('humidity', 'N/A')}%")
    print(f"Dew Point: {current_data.get('dew_point', 'N/A')}°C")
    print(f"Cloudiness: {current_data.get('clouds', 'N/A')}%")
    print(f"UV Index: {current_data.get('uvi', 'N/A')}")
    print(f"Visibility: {current_data.get('visibility', 'N/A')} metres")
    print("-" * 20)

    # Wind
    print(f"Wind Speed: {current_data.get('wind_speed', 'N/A')} m/s")
    print(f"Wind Direction: {current_data.get('wind_deg', 'N/A')}°")
    if 'wind_gust' in current_data:
        print(f"Wind Gust: {current_data.get('wind_gust')} m/s")
    print("-" * 20)

    # Precipitation (only appears when it's raining/snowing)
    if 'rain' in current_data and '1h' in current_data['rain']:
        print(f"Rain (last hour): {current_data['rain']['1h']} mm/h")
    if 'snow' in current_data and '1h' in current_data['snow']:
        print(f"Snow (last hour): {current_data['snow']['1h']} mm/h")

# This block runs only when the script is executed directly
if __name__ == "__main__":
    load_dotenv()
    
    # Get coordinates for the location
    lat, lon = get_coordinates()
    
    # Fetch the weather data
    if lat is not None and lon is not None:
        weather_data = fetch_current_ep(lat, lon)
        
        # If data is fetched successfully, display it
        if weather_data:
            display_weather(weather_data)
            # You can also uncomment the lines below to see the raw JSON
            # print("\n--- Raw JSON Data ---")
            # print(json.dumps(weather_data, indent=2))

import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
lat = 33.44
lon = -94.04
api_key = os.getenv("OPEN_WEATHER_API_KEY")
exclude_parts = "minutely,hourly,daily,alerts"

url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}&units=metric"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    output_filename = "currentep.json"
    with open(output_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # confirmation message 
    print(f"Data saved to {output_filename}")
    print("=" * 30) # Separator for clarity


    # PRINT BLOCK 
    print("--- Detailed Current Weather ---")
    current_data = data.get('current', {})
    ''' print(json.dumps(data, indent=2))
    #Example: Get the current temperature
        current_temp = data['current']['temp']
        print(f"Current Temperature: {current_temp}°C") 
    '''  
    if not current_data:
        print("'current' data block is not available.")
    else:
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
        # Safely access wind_gust, as it's not always present
    if 'wind_gust' in current_data:
        print(f"Wind Gust: {current_data.get('wind_gust')} m/s")
        print("-" * 20)

        # Precipitation (only appears when it's raining/snowing)
    if 'rain' in current_data and '1h' in current_data['rain']:
        print(f"Rain (last hour): {current_data['rain']['1h']} mm/h")
    if 'snow' in current_data and '1h' in current_data['snow']:
        print(f"Snow (last hour): {current_data['snow']['1h']} mm/h")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"A request error occurred: {req_err}")
except KeyError:
    print("Error: A key was not found in the response. Check the API documentation and your subscription.")
    if 'data' in locals():
        print("Server Response:", json.dumps(data, indent=2))
except Exception as e:
    print(f"An unexpected error occurred: {e}")

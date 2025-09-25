import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Assuming get_coordinates is in a file named app.py in the same directory.
# If it's not, you might need to adjust the import.
try:
    from app import get_coordinates
except ImportError:
    print("Warning: 'app.py' not found. You'll need to provide coordinates manually.")
    # Define a dummy function if app.py is not available
    def get_coordinates():
        print("Please implement the get_coordinates function.")
        return None, None

# --- Constants for Severe Weather Analysis ---
WIND_SPEED_THRESHOLD_MS = 33  # 33 m/s = ~119 km/h, Category 1 storm
PRESSURE_THRESHOLD_HPA = 980  # Extremely low pressure

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

    # ... (rest of the display_weather function is unchanged)
    weather_info = current_data.get('weather', [{}])[0]
    print(f"Condition: {weather_info.get('description', 'N/A').title()}")
    print("-" * 20)
    print(f"Temperature: {current_data.get('temp', 'N/A')}°C")
    print(f"Feels Like: {current_data.get('feels_like', 'N/A')}°C")
    print(f"Pressure: {current_data.get('pressure', 'N/A')} hPa")
    print(f"Humidity: {current_data.get('humidity', 'N/A')}%")
    print(f"Dew Point: {current_data.get('dew_point', 'N/A')}°C")
    print(f"Cloudiness: {current_data.get('clouds', 'N/A')}%")
    print(f"UV Index: {current_data.get('uvi', 'N/A')}")
    print(f"Visibility: {current_data.get('visibility', 'N/A')} metres")
    print("-" * 20)
    print(f"Wind Speed: {current_data.get('wind_speed', 'N/A')} m/s")
    print(f"Wind Direction: {current_data.get('wind_deg', 'N/A')}°")
    if 'wind_gust' in current_data:
        print(f"Wind Gust: {current_data.get('wind_gust')} m/s")
    print("-" * 20)
    if 'rain' in current_data and '1h' in current_data['rain']:
        print(f"Rain (last hour): {current_data['rain']['1h']} mm/h")
    if 'snow' in current_data and '1h' in current_data['snow']:
        print(f"Snow (last hour): {current_data['snow']['1h']} mm/h")

def generate_weather_advice(current_weather, daily_forecast):
    """
    Generates human-readable advice based on weather data.
    This acts as our 'AI' logic.
    """
    advice = []
    
    # Extract key metrics for decision making
    uvi = current_weather.get('uvi', 0)
    pop = daily_forecast.get('pop', 0) * 100  # Probability of precipitation
    day_temp = daily_forecast.get('temp', {}).get('day', 0)
    weather_condition = daily_forecast.get('weather', [{}])[0].get('main', '')

    # Advice based on UV Index
    if uvi > 7:
        advice.append(f"The UV index is high ({uvi}). Wear sunscreen and sunglasses if you'll be outside for a while.")
    elif uvi > 2:
        advice.append(f"The UV index is moderate ({uvi}). It's still a good idea to protect your skin.")

    # Advice based on precipitation
    if pop > 60:
        advice.append(f"There's a high chance of rain today ({pop:.0f}%). Don't forget your umbrella!")
    elif pop > 30:
        advice.append(f"There's a slight chance of rain ({pop:.0f}%). It might be a good idea to take an umbrella just in case.")

    # Advice based on temperature
    if day_temp > 32:
        advice.append(f"It's going to be very hot, around {day_temp}°C. Stay hydrated and avoid strenuous activity during peak hours.")
    
    # Advice based on general weather conditions
    if weather_condition == "Thunderstorm":
        advice.append("Thunderstorms are expected. It's best to stay indoors and avoid open areas.")
    elif weather_condition == "Clear":
        advice.append("Expect clear skies today, a perfect day for outdoor activities!")
    elif weather_condition in ["Rain", "Drizzle"]:
        advice.append("Rain is expected. Wear waterproof clothing if you plan to be outside.")

    # Default message if no other advice fits
    if not advice:
        advice.append("Weather conditions seem stable today. Enjoy your day!")

    return advice


def fetch_and_generate_advice(lat, lon, api_key):
    """
    Fetches weather data, generates advice, and returns it as a JSON object.
    """
    exclude_parts = "minutely,hourly,alerts"
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_data = data.get('current', {})
        today_daily_data = data['daily'][0]

        advice_list = generate_weather_advice(current_data, today_daily_data)
        friendly_summary = today_daily_data.get('summary', "A general weather overview for the day.")

        assistant_output = {
            "location": {
                "latitude": lat,
                "longitude": lon,
                "timezone": data.get('timezone', 'N/A')
            },
            "assistant_report": {
                "generated_at_utc": datetime.utcfromtimestamp(current_data.get('dt')).isoformat() + 'Z',
                "friendly_summary": friendly_summary,
                "advice": advice_list,
                "key_metrics": {
                    "current_temp_celsius": current_data.get('temp'),
                    "current_condition": current_data.get('weather', [{}])[0].get('description', 'N/A').title(),
                    "chance_of_rain_percent": today_daily_data.get('pop', 0) * 100,
                    "max_temp_celsius": today_daily_data.get('temp', {}).get('max'),
                    "min_temp_celsius": today_daily_data.get('temp', {}).get('min')
                }
            }
        }
        return assistant_output

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except (KeyError, IndexError):
        print("Error: Could not parse the weather data from the API response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

def monitor_and_analyze_severe_weather(lat, lon, api_key):
    """
    Fetches weather data and analyzes it for severe conditions (cyclones)
    in a clear, hierarchical order. Returns the final analysis as a JSON object.
    """
    # 1. Initialize the report structure. This will be updated as we go.
    analysis_report = {
        "timestamp_utc": datetime.utcnow().isoformat() + 'Z',
        "monitoring_location": {"latitude": lat, "longitude": lon},
        "status": "UNKNOWN", # Default status
        "details": {}
    }

    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric'}
    
    # 2. Fetch data from the API. If it fails, update the report and return immediately.
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        analysis_report["status"] = "API_ERROR"
        analysis_report["details"]["message"] = f"API request failed: {e}"
        # This is the final report in case of an API error.
        return analysis_report
        
    # 3. Check for official alerts first. This has the highest priority.
    if 'alerts' in data:
        for alert in data['alerts']:
            event_name = alert.get('event', '').lower()
            if any(keyword in event_name for keyword in ['cyclone', 'hurricane', 'typhoon', 'tropical storm']):
                analysis_report["status"] = "OFFICIAL_ALERT"
                analysis_report["details"]["message"] = "Official severe weather alert issued!"
                analysis_report["details"]["alert_data"] = alert
                # This is the final report because an official alert overrides everything else.
                return analysis_report
    
    # 4. If no official alerts, proceed to analyze the real-time conditions.
    current_weather = data.get('current', {})
    current_wind = current_weather.get('wind_speed', 0)
    current_pressure = current_weather.get('pressure', 1013)

    analysis_report["details"]["current_weather"] = {
        "wind_speed_ms": current_wind,
        "pressure_hpa": current_pressure
    }

    # This logic block determines the final status based on thresholds.
    if current_wind > WIND_SPEED_THRESHOLD_MS and current_pressure < PRESSURE_THRESHOLD_HPA:
        analysis_report["status"] = "DANGER_CONDITIONS_MET"
        analysis_report["details"]["message"] = "High-danger: Sustained high winds and extremely low pressure detected."
    elif current_wind > WIND_SPEED_THRESHOLD_MS:
        analysis_report["status"] = "CAUTION_HIGH_WINDS"
        analysis_report["details"]["message"] = "Caution: Extremely high wind speeds detected."
    elif current_pressure < PRESSURE_THRESHOLD_HPA:
        analysis_report["status"] = "CAUTION_LOW_PRESSURE"
        analysis_report["details"]["message"] = "Caution: Extremely low atmospheric pressure detected."
    else:
        analysis_report["status"] = "CLEAR"
        analysis_report["details"]["message"] = "No immediate cyclone indicators found in current conditions."
        
    # 5. This is the final report based on the analysis of current conditions.
    return analysis_report


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    
    if not api_key:
        print("Error: OPEN_WEATHER_API_KEY not found in .env file.")
    else:
        lat, lon = get_coordinates()
        
        if lat is not None and lon is not None:
            # --- Original functionality: Display current weather ---
            weather_data = fetch_current_ep(lat, lon)
            if weather_data:
                display_weather(weather_data)

            # --- AI Assistant functionality ---
            print("\n" + "=" * 30)
            print("--- AI Weather Assistant Report ---")
            advice_json = fetch_and_generate_advice(lat, lon, api_key)
            if advice_json:
                print(json.dumps(advice_json, indent=4))
            
            # --- Severe Weather Monitoring functionality ---
            print("\n" + "=" * 30)
            print("--- Severe Weather Analysis ---")
            severe_weather_report = monitor_and_analyze_severe_weather(lat, lon, api_key)
            if severe_weather_report:
                print(json.dumps(severe_weather_report, indent=4))


import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from app import get_coordinates

#  Configuration and Setup

# Load your API key
load_dotenv()
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# Coordinates 
lat, lon = get_coordinates()
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

# Define the danger thresholds for cyclone conditions
WIND_SPEED_THRESHOLD_MS = 33  # 33 m/s = ~119 km/h, Category 1 storm
PRESSURE_THRESHOLD_HPA = 980  # Extremely low pressure

def save_to_json(data):
    """Saves the provided dictionary data to a timestamped JSON file."""
    # Generate a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"majoralert_{timestamp}.json"

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f" Analysis complete. Report saved to: {filename}")

def monitor_severe_weather(lat, lon, api_key):
    """
    Fetches weather data, analyzes it for severe conditions,
    and saves the findings to a JSON file.
    """
    if not api_key:
        print("Error: API key not found. Please check your .env file.")
        return

    # Prepare the analysis report dictionary
    analysis_report = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "monitoring_location": {"latitude": lat, "longitude": lon},
        "status": "UNKNOWN",
        "details": {}
    }

    params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric'}
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        analysis_report["status"] = "API_ERROR"
        analysis_report["details"]["message"] = f"API request failed: {e}"
        save_to_json(analysis_report)
        return
        
    # --- Step 2: Check for Official Alerts (Highest Priority) ---
    if 'alerts' in data:
        for alert in data['alerts']:
            event_name = alert.get('event', '').lower()
            if any(keyword in event_name for keyword in ['cyclone', 'hurricane', 'typhoon', 'tropical storm']):
                analysis_report["status"] = "OFFICIAL_ALERT"
                analysis_report["details"]["message"] = "Official severe weather alert issued!"
                analysis_report["details"]["alert_data"] = alert
                save_to_json(analysis_report)
                return # Exit after finding a definitive alert
    
    # --- Step 3: Analyze Real-time Weather Data ---
    current_weather = data.get('current', {})
    current_wind = current_weather.get('wind_speed', 0)
    current_pressure = current_weather.get('pressure', 1013)

    analysis_report["details"]["current_weather"] = {
        "wind_speed_ms": current_wind,
        "pressure_hpa": current_pressure
    }

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
        
    save_to_json(analysis_report)

# --- Run the main function ---
if __name__ == "__main__":
    monitor_severe_weather(lat, lon, API_KEY)
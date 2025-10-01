from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import math
from geo_module import get_city_coords

# --- Import your data processing scripts here ---
# from python.wsummary import get_weather_summary
# from python.majoralert import get_major_alerts
# from python.generalalert import get_general_alerts

# Load .env file
load_dotenv(dotenv_path='./python/.env')

# Initialize Flask & OpenAI
app = Flask(_name_)
CORS(app)  # Enable CORS for all routes
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory cache for coordinates
cache = {}
CACHE_TTL = 300  # Cache time-to-live in seconds (5 minutes)

# --- NEW: The Main Endpoint for Live Data ---
@app.route("/api/live-alerts", methods=["GET"])
def get_live_alerts():
    """
    This is the main endpoint your frontend will poll every 15 seconds.
    It should call your other python scripts to get live data.
    """
    try:
        # 1. Get city from query parameters, with a default value
        city = request.args.get("city", "mumbai") # Default to a city for testing

        # 2. Call the imported functions from your other scripts
        # (These function names are examples, change them to match your actual scripts)
        # weather_summary = get_weather_summary(city)
        # major_alerts = get_major_alerts(city)
        # general_alerts = get_general_alerts(city)

        # 3. For now, we'll use placeholder mock data
        mock_data = {
            "weather_summary": {"temp": "28°C", "condition": "Partly Cloudy"},
            "major_alerts": [{"id": 1, "type": "Tsunami Warning", "level": "High"}],
            "general_alerts": [{"id": 1, "type": "High Tide", "level": "Moderate"}]
        }

        # 4. Combine the data into a single JSON response
        return jsonify({
            "city": city,
            "timestamp": time.time(),
            "data": mock_data # In the future, replace mock_data with real data
            # "data": {
            #    "weather_summary": weather_summary,
            #    "major_alerts": major_alerts,
            #    "general_alerts": general_alerts
            # }
        })

    except Exception as e:
        # Log the error for debugging
        print(f"Error in /api/live-alerts: {e}")
        return jsonify({"error": "Failed to fetch live alert data", "details": str(e)}), 500


# --- Your Existing Utility Endpoints (with fixes) ---

@app.route("/get-coordinates", methods=["POST"])
def get_coordinates():
    data = request.get_json()
    p_id = data.get("_id")
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    city = city.lower().strip()

    # Check cache first
    if (p_id, city) in cache and time.time() - cache[(p_id, city)]["timestamp"] < CACHE_TTL:
        return jsonify({
            "coordinates": cache[(p_id, city)]["coords"],
            "cached": True
        })

    # If not in cache or expired, fetch new data
    coords_dict = get_city_coords(city)

    if coords_dict is None:
        return jsonify({"error": "Failed to retrieve coordinates."}), 500

    coords_list = [coords_dict["latitude"], coords_dict["longitude"]]
    
    # Update cache
    cache[(p_id, city)] = {
        "coords": coords_list,
        "timestamp": time.time()
    }

    return jsonify({
        "coordinates": coords_list,
        "cached": False
    })

@app.route("/getmaxmin-coordinates", methods=["GET"])
def getmaxmin_coordinates():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    coords_dict = get_city_coords(city)

    if coords_dict is None:
        return jsonify({"error": "Failed to retrieve coordinates."}), 500

    lat = coords_dict["latitude"]
    lon = coords_dict["longitude"]

    # Define a bounding box
    delta = 0.1
    lat_min = lat - delta
    lat_max = lat + delta
    lon_min = lon - delta
    lon_max = lon + delta

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in kilometers
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)*2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)*2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    diagonal = haversine(lat_min, lon_min, lat_max, lon_max)
    radius = round(diagonal / 2, 2)

    return jsonify({
        "coordinates": {
            "lat_min": round(lat_min, 2),
            "lat_max": round(lat_max, 2),
            "lon_min": round(lon_min, 2),
            "lon_max": round(lon_max, 2),
        },
        "Radius_km": radius
    })

@app.route("/get-emergency-contact", methods=["POST"])
def get_emergency_contact():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    city = city.lower().strip()

    try:
        prompt = (
            f"What is the general emergency contact number (police/fire/ambulance) for {city}? "
            f"Reply with only the number and the service, e.g., '112 – General emergency'."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides emergency contact numbers only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=50
        )

        emergency_info = response.choices[0].message.content.strip()

        return jsonify({
            "city": city,
            "emergency_contact": emergency_info
        })

    except Exception as e:
        return jsonify({"error": "Failed to fetch emergency contact", "details": str(e)}), 500


if _name_ == '_main_':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re, json,time
import math

# Load .env file
load_dotenv()

# Initialize Flask & OpenAI
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cache = {}
CACHE_TTL = 300 


@app.route("/get-coordinates", methods=["POST"])
def get_coordinates():
    data = request.get_json()
    p_id=data.get("_id")
    city = data.get("city")
    
    if not city:
        return jsonify({"error": "City is required"}), 400

    city = city.lower().strip()  # normalize city name

    # ✅ Check cache
    if (p_id,city) in cache:
        cached_data = cache[(p_id,city)]
        if time.time() - cached_data["timestamp"] < CACHE_TTL:
            # Return cached result if less than 5 minutes old
            return jsonify({
                "coordinates": cached_data["coords"],
                "cached": True
            })

    # ❌ Not in cache OR expired → Call OpenAI
    # Ask AI for coordinates
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a geolocation assistant. Return only JSON with latitude and longitude of the city, rounded to 2 decimal places."},
            {"role": "user", "content": f"Give me latitude and longitude of {city} in JSON format with keys latitude and longitude."}
        ]
    )

    # Extract AI reply
    ai_reply = response.choices[0].message.content
    ai_reply = re.sub(r"```json|```", "", ai_reply).strip()

    # Example AI reply: {"latitude": 13.0827, "longitude": 80.2707}
    try:
        coords_dict = json.loads(ai_reply)  # Convert string JSON → dict (safe if AI structured properly)
        lat = round(float(coords_dict["latitude"]), 2)
        lon = round(float(coords_dict["longitude"]), 2)
        coords_list = [lat, lon]
    except Exception as e:
        return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500
    
    # ✅ Save in cache
    cache[(p_id,city)] = {
        "coords": coords_list,
        "timestamp": time.time()
    }

    return jsonify({
        "coordinates": coords_list,
        "cached": False
    })
    
@app.route("/getmaxmin-coordinates", methods=["GET"])
def getmaxmin_coordinates():
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a geolocation assistant. Return only JSON with latitude and longitude of the city, rounded to 2 decimal places."},
        {"role": "user", "content": f"Give me latitude and longitude of  in JSON format with keys latitude and longitude."}
        ]
    )
    ai_reply = response.choices[0].message.content
    ai_reply = re.sub(r"json|", "", ai_reply).strip()
    try:
        coords_dict = json.loads(ai_reply)
        lat = round(float(coords_dict["latitude"]), 2)
        lon = round(float(coords_dict["longitude"]), 2)

    # Define bounding box offsets (approx 0.1° ≈ 11 km in lat, ~11 km * cos(lat) in lon)
        delta = 0.1  

        lat_min = lat - delta
        lat_max = lat + delta
        lon_min = lon - delta
        lon_max = lon + delta

    # Haversine formula to calculate max radius (diagonal corner distance / 2)
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth radius in km
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            dphi = math.radians(lat2 - lat1)
            dlambda = math.radians(lon2 - lon1)

            a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
            return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))  
            coords_list = [lat1, lon1,lat2,lon2]
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

    except Exception as e:
        return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500
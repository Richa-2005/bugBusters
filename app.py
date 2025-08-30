from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re, json,time

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
    city = data.get("city")
    
    if not city:
        return jsonify({"error": "City is required"}), 400

    city = city.lower().strip()  # normalize city name

    # ✅ Check cache
    if city in cache:
        cached_data = cache[city]
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
    ai_reply = response.choices[0].message["content"]
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
    cache[city] = {
        "coords": coords_list,
        "timestamp": time.time()
    }

    return jsonify({
        "coordinates": coords_list,
        "cached": False
    })
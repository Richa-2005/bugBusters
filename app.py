# # app.py
# from flask import Flask, request, jsonify
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# import re, json, time
# import math
# from geo_module import get_city_coords

# # Load .env file
# load_dotenv()

# # Initialize Flask & OpenAI
# app = Flask(__name__)
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# cache = {}
# CACHE_TTL = 300 #300sec->5min

# @app.route("/get-coordinates", methods=["POST"])
# def get_coordinates():
#     data = request.get_json()
#     p_id = data.get("_id")
#     city = data.get("city")
    
#     if not city:
#         return jsonify({"error": "City is required"}), 400

#     city = city.lower().strip()

#     if (p_id, city) in cache:
#         cached_data = cache[(p_id, city)]
#         if time.time() - cached_data["timestamp"] < CACHE_TTL:
#             return jsonify({
#                 "coordinates": cached_data["coords"],
#                 "cached": True
#             })

#     coords_dict = get_city_coords(city)

#     if coords_dict is None:
#         return jsonify({"error": "Failed to retrieve coordinates."}), 500
    
#     coords_list = [coords_dict["latitude"], coords_dict["longitude"]]
#     cache[(p_id, city)] = {
#         "coords": coords_list,
#         "timestamp": time.time()
#     }

#     return jsonify({
#         "coordinates": coords_list,
#         "cached": False
#     })

# @app.route("/getmaxmin-coordinates", methods=["GET"])
# def getmaxmin_coordinates():
#     # Use request.args.get() to get data from a query parameter
#     city = request.args.get("city")
#     if not city:
#         return jsonify({"error": "City is required"}), 400

#     coords_dict = get_city_coords(city)

#     if coords_dict is None:
#         return jsonify({"error": "Failed to retrieve coordinates."}), 500

#     lat = coords_dict["latitude"]
#     lon = coords_dict["longitude"]
    
#     delta = 0.1
#     lat_min = lat - delta
#     lat_max = lat + delta
#     lon_min = lon - delta
#     lon_max = lon + delta

#     def haversine(lat1, lon1, lat2, lon2):
#         R = 6371
#         phi1, phi2 = math.radians(lat1), math.radians(lat2)
#         dphi = math.radians(lat2 - lat1)
#         dlambda = math.radians(lon2 - lon1)
#         a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
#         return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
#     diagonal = haversine(lat_min, lon_min, lat_max, lon_max)
#     radius = round(diagonal / 2, 2)

#     return jsonify({
#         "coordinates": {
#             "lat_min": round(lat_min, 2),
#             "lat_max": round(lat_max, 2),
#             "lon_min": round(lon_min, 2),
#             "lon_max": round(lon_max, 2),
#         },
#         "Radius_km": radius
#     })

# @app.route("/get-emergency-contact", methods=["POST"])
# def get_emergency_contact():
#     data = request.get_json()
#     city = data.get("city")

#     if not city:
#         return jsonify({"error": "City is required"}), 400

#     city = city.lower().strip()

#     try:
#         prompt = (
#             f"What is the general emergency contact number (police/fire/ambulance) for {city}? "
#             f"Reply with only the number and the service, e.g., '112 – General emergency'."
#         )

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that provides emergency contact numbers only."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2,
#             max_tokens=50
#         )

#         emergency_info = response.choices[0].message.content.strip()

#         return jsonify({
#             "city": city,
#             "emergency_contact": emergency_info
#         })

#     except Exception as e:
#         return jsonify({"error": "Failed to fetch emergency contact", "details": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re, json, time
import math
from geo_module import get_city_coords
from flask_cors import CORS # Import CORS from the flask_cors library

# Load .env file
load_dotenv()

# Initialize Flask & OpenAI
app = Flask(__name__)
# Enable CORS for all routes and origins
# You can restrict this to specific origins for better security in a production environment.
# For local development, '*' is fine.
CORS(app) 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cache = {}
CACHE_TTL = 300 #300sec->5min

@app.route("/get-coordinates", methods=["POST"])
def get_coordinates():
    data = request.get_json()
    p_id = data.get("_id")
    city = data.get("city")
    
    if not city:
        return jsonify({"error": "City is required"}), 400

    city = city.lower().strip()

    if (p_id, city) in cache:
        cached_data = cache[(p_id, city)]
        if time.time() - cached_data["timestamp"] < CACHE_TTL:
            return jsonify({
                "coordinates": cached_data["coords"],
                "cached": True
            })

    coords_dict = get_city_coords(city)

    if coords_dict is None:
        return jsonify({"error": "Failed to retrieve coordinates."}), 500
    
    coords_list = [coords_dict["latitude"], coords_dict["longitude"]]
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
    # Use request.args.get() to get data from a query parameter
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    coords_dict = get_city_coords(city)

    if coords_dict is None:
        return jsonify({"error": "Failed to retrieve coordinates."}), 500

    lat = coords_dict["latitude"]
    lon = coords_dict["longitude"]
    
    delta = 0.1
    lat_min = lat - delta
    lat_max = lat + delta
    lon_min = lon - delta
    lon_max = lon + delta

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
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
            model="gpt-4o",
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

if __name__ == '__main__':
    app.run(debug=True)

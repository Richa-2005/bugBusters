# geo_module.py
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_city_coords(city):
    """
    Fetches the latitude and longitude of a city using an AI assistant.
    Returns a dictionary with 'latitude' and 'longitude' or None on failure.
    """
    if not city:
        return None

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a geolocation assistant. Return only JSON with latitude and longitude of the city, rounded to 2 decimal places."},
            {"role": "user", "content": f"Give me latitude and longitude of {city} in JSON format with keys latitude and longitude."}
        ]
    )

    ai_reply = response.choices[0].message.content
    ai_reply = re.sub(r"```json|```", "", ai_reply).strip()

    try:
        coords_dict = json.loads(ai_reply)
        lat = round(float(coords_dict["latitude"]), 2)
        lon = round(float(coords_dict["longitude"]), 2)
        
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return None
import pandas as pd
import json
import requests
from datetime import datetime
from app import getmaxmin_coordinates
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

# CONFIGURATION
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY was not found. Check your api.env file.")
genai.configure(api_key=api_key)


# 2. Define data sources and outputs
INPUT_CSV_PATH = 'historical_tsunamis.csv'
OUTPUT_JSON_REPORT_PATH = 'comprehensive_tsunami_report.json'
# The base URL is now more flexible to allow for location-specific queries
USGS_API_URL_BASE = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"

# 3. Define the geographical bounding boxes for high-risk zones
REGIONS = {
    "Japan-Kuril Trench": [140, 30, 160, 50],
    "Sunda Arc (Indonesia)": [95, -10, 125, 6],
    "Chile-Peru Trench": [-80, -45, -70, -18],
    "Cascadia Subduction Zone": [-130, 40, -122, 50]
}

def analyze_historical_data(file_path):
    """Analyzes the CSV to generate historical risk rules."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return None
    tsunami_events = df[df['tsunami'] == 1].copy()
    risk_rules = []
    for region_name, bounds in REGIONS.items():
        min_lon, min_lat, max_lon, max_lat = bounds
        region_df = tsunami_events[
            (tsunami_events['longitude'] >= min_lon) & (tsunami_events['longitude'] <= max_lon) &
            (tsunami_events['latitude'] >= min_lat) & (tsunami_events['latitude'] <= max_lat)
        ]
        if not region_df.empty:
            rule = {
                "region_name": region_name,
                "bounds": {"min_lon": min_lon, "min_lat": min_lat, "max_lon": max_lon, "max_lat": max_lat},
                "min_magnitude": round(region_df['magnitude'].min(), 1),
                "max_depth": round(region_df['depth'].max(), 1)
            }
            risk_rules.append(rule)
    return risk_rules

def fetch_earthquake_for_location(target_coords):
    """Fetches the most recent significant earthquake near the target coordinates."""
    # Build the query URL with location parameters
    params = {
        'latitude': target_coords['lat'],
        'longitude': target_coords['lon'],
        'maxradiuskm': target_coords['radius_km']
    }
    try:
        response = requests.get(USGS_API_URL_BASE, params=params, timeout=15)
        response.raise_for_status()
        features = response.json().get('features', [])
        if features:
            # The API returns them sorted by time, so the first is the most recent
            return features[0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching USGS data for the specified location: {e}")
    return None

def perform_initial_assessment(earthquake, rules):
    """Performs a preliminary risk assessment based on historical rules."""
    props = earthquake['properties']
    geom = earthquake['geometry']['coordinates']
    lon, lat, depth = geom[0], geom[1], geom[2]
    mag = props['mag']
    
    for rule in rules:
        bounds = rule['bounds']
        if (bounds['min_lon'] <= lon <= bounds['max_lon'] and
            bounds['min_lat'] <= lat <= bounds['max_lat']):
            if mag >= rule['min_magnitude'] and depth <= rule['max_depth']:
                return {
                    "risk_level": "HIGH",
                    "reason": f"Event matches the high-risk profile for the '{rule['region_name']}'."
                }
    return {
        "risk_level": "LOW",
        "reason": "Event does not match any known high-risk historical profiles."
    }

def get_gemini_analysis(earthquake_data, assessment, historical_rules):
    """Generates a prompt and gets analysis from the Gemini API."""
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        return {"error": "Gemini API key not configured."}

    # Construct the detailed prompt
    prompt = f"""
    Act as a senior seismologist and disaster management expert.
    
    **Historical Context:**
    My system has analyzed a historical earthquake dataset and generated the following risk profiles for tsunami generation in specific regions:
    {json.dumps(historical_rules, indent=2)}

    **Real-Time Seismic Event:**
    A new earthquake has just been detected with the following details:
    - Location: {earthquake_data['properties']['place']}
    - Magnitude: {earthquake_data['properties']['mag']}
    - Depth: {earthquake_data['geometry']['coordinates'][2]} km
    - Time: {datetime.fromtimestamp(earthquake_data['properties']['time'] / 1000)} UTC

    **Initial Computer Assessment:**
    My rule-based system made an initial assessment: {assessment['risk_level']} - {assessment['reason']}

    **Your Task:**
    Based on all the information above (historical context, real-time data, and the initial assessment), provide a concise analysis in JSON format. The JSON object must have three keys: "summary", "alerts", and "suggestions".
    - "summary": A brief, one-sentence overview of the situation.
    - "alerts": A list of 2-3 critical, immediate warning messages for the public and authorities. Mention the concept of deep-ocean buoy activation (like DART) if the event is a significant undersea earthquake.
    - "suggestions": A list of 2-3 actionable recommendations for safety and monitoring.
    
    Provide only the raw JSON object as your response.
    """

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        
        full_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        json_text = full_text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except (KeyError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse Gemini response: {e}", "raw_response": full_text}

def main():
    """Main function to generate the comprehensive report."""
    print("--- Starting Comprehensive Tsunami Report Generation ---")
    
    # 1. Get the target coordinates from the external file
    target_location = get_coordinates()
    print(f"Monitoring location set to: {target_location['name']} (Lat: {target_location['lat']}, Lon: {target_location['lon']})")

    # 2. Analyze historical data
    risk_rules = analyze_historical_data(INPUT_CSV_PATH)
    if not risk_rules:
        print(f"Could not analyze historical data from '{INPUT_CSV_PATH}'. Exiting.")
        return

    # 3. Fetch the latest earthquake for the specified location
    location_earthquake = fetch_earthquake_for_location(target_location)
    
    # 4. Build the final report
    report = {
        "report_generated_utc": datetime.utcnow().isoformat(),
        "monitoring_location": target_location,
        "historical_context": {"source_file": INPUT_CSV_PATH, "derived_rules": risk_rules},
        "real_time_event": {},
        "initial_assessment": {},
        "gemini_analysis": {}
    }

    if location_earthquake:
        print(f"Found a recent event near target: M{location_earthquake['properties']['mag']} at {location_earthquake['properties']['place']}")
        report["real_time_event"] = {
            "status": "Earthquake Detected Near Target Location",
            "data": location_earthquake
        }
        
        # 5. Perform initial assessment
        assessment = perform_initial_assessment(location_earthquake, risk_rules)
        report["initial_assessment"] = assessment
        print(f"Initial Assessment: {assessment['risk_level']} - {assessment['reason']}")

        # 6. Get Gemini's expert analysis
        print("Querying Gemini API for expert analysis...")
        gemini_output = get_gemini_analysis(location_earthquake, assessment, risk_rules)
        report["gemini_analysis"] = gemini_output
    else:
        print(f"No significant earthquakes detected within {target_location['radius_km']}km of the target in the last 24 hours.")
        report["real_time_event"]["status"] = "No significant earthquake detected near target."

    # 7. Save the final JSON report
    with open(OUTPUT_JSON_REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=4)
    
    print(f"\n--- Report generation complete. Output saved to '{OUTPUT_JSON_REPORT_PATH}' ---")

if __name__ == "__main__":
    main()



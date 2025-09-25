import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(dotenv_path='.env')

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY was not found. Check your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# File paths
INPUT_CSV_PATH = 'historical_tsunamis.csv'
OUTPUT_JSON_REPORT_PATH = 'comprehensive_tsunami_report.json'

# USGS API for real-time earthquakes
USGS_API_URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# High-risk regions
REGIONS = {
    "Japan-Kuril Trench": [140, 30, 160, 50],
    "Sunda Arc (Indonesia)": [95, -10, 125, 6],
    "Chile-Peru Trench": [-80, -45, -70, -18],
    "Cascadia Subduction Zone": [-130, 40, -122, 50]
}

def analyze_historical_data(file_path):
    """Analyze historical tsunami events to create region-specific risk rules."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.")
        return None

    df.columns = [col.strip().lower() for col in df.columns]
    column_mapping = {
        'latitude': 'latitude',
        'longitude': 'longitude',
        'earthquake magnitude': 'magnitude',
        'maximum water height (m)': 'depth',
        'tsunami event validity': 'tsunami'
    }
    df = df.rename(columns=column_mapping)

    required_columns = {'tsunami', 'latitude', 'longitude', 'magnitude', 'depth'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"❌ CSV is missing required columns. Required: {required_columns}")

    df['tsunami'] = pd.to_numeric(df['tsunami'], errors='coerce').fillna(0).astype(int)
    tsunami_events = df[df['tsunami'] == 1].copy()

    risk_rules = []
    for region_name, (min_lon, min_lat, max_lon, max_lat) in REGIONS.items():
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

def fetch_earthquake_for_location(coords):
    """Fetch recent earthquake data near given coordinates."""
    params = {
        'format': 'geojson',
        'latitude': coords['lat'],
        'longitude': coords['lon'],
        'maxradiuskm': coords['radius_km'],
        'minmagnitude': 4.5,
        'orderby': 'time',
        'limit': 1
}

    try:
        response = requests.get(USGS_API_URL_BASE, params=params, timeout=15)
        response.raise_for_status()
        features = response.json().get('features', [])
        return features[0] if features else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching USGS data: {e}")
        return None

def perform_initial_assessment(event, rules):
    """Assess tsunami risk using historical rules."""
    lon, lat, depth = event['geometry']['coordinates']
    mag = event['properties']['mag']

    for rule in rules:
        b = rule['bounds']
        if b['min_lon'] <= lon <= b['max_lon'] and b['min_lat'] <= lat <= b['max_lat']:
            if mag >= rule['min_magnitude'] and depth <= rule['max_depth']:
                return {
                    "risk_level": "HIGH",
                    "reason": f"Matches high-risk profile for {rule['region_name']}."
                }
    return {
        "risk_level": "LOW",
        "reason": "No match with high-risk regions."
    }

def get_gemini_analysis(earthquake, assessment, rules):
    """Get expert-like JSON analysis from Gemini."""
    prompt = f"""
    You are a senior seismologist and disaster management expert.

    **Historical Risk Rules:**
    {json.dumps(rules, indent=2)}

    **Recent Earthquake:**
    - Location: {earthquake['properties']['place']}
    - Magnitude: {earthquake['properties']['mag']}
    - Depth: {earthquake['geometry']['coordinates'][2]} km
    - Time: {datetime.fromtimestamp(earthquake['properties']['time'] / 1000)} UTC

    **Initial System Assessment:**
    {assessment['risk_level']} - {assessment['reason']}

    **Your Task:**
    Based on all the information above, provide a concise analysis in JSON format. The JSON object must have three keys: "summary", "alerts", and "suggestions".
    - "summary": A brief, one-sentence overview of the situation.
    - "alerts": A list of 2-3 critical, immediate warning messages. Mention deep-ocean buoy activation (like DART).
    - "suggestions": A list of 2-3 actionable recommendations for safety and monitoring.
    
    Provide only the raw JSON object as your response.
    
    """
    
     # --- THIS LINE IS CORRECTED ---
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    # --- END OF CORRECTION ---

    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        full_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        json_text = full_text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
    except Exception as e:
        return {"error": f"Gemini response error: {e}"}

def main():
    print("--- Starting Tsunami Report Generation ---")

    target_location = {
        "name": "Offshore Honshu, Japan",
        "lat": 38.322,
        "lon": 142.369,
        "radius_km": 500
    }
    print(f"Monitoring: {target_location['name']}")

    risk_rules = analyze_historical_data(INPUT_CSV_PATH)
    if not risk_rules:
        print("No historical rules generated. Exiting.")
        return

    earthquake = fetch_earthquake_for_location(target_location)

    report = {
        "report_generated_utc": datetime.utcnow().isoformat(),
        "monitoring_location": target_location,
        "historical_context": {"source_file": INPUT_CSV_PATH, "derived_rules": risk_rules},
        "real_time_event": {},
        "initial_assessment": {},
        "gemini_analysis": {}
    }

    if earthquake:
        print(f"Recent Earthquake: M{earthquake['properties']['mag']} at {earthquake['properties']['place']}")
        report["real_time_event"] = {
            "status": "Alert!!! Earthquake Detected",
            "data": earthquake
        }

        assessment = perform_initial_assessment(earthquake, risk_rules)
        report["initial_assessment"] = assessment
        print(f"Assessment: {assessment['risk_level']} - {assessment['reason']}")

        gemini_result = get_gemini_analysis(earthquake, assessment, risk_rules)
        report["gemini_analysis"] = gemini_result
    else:
        print("No recent significant earthquake detected.")
        report["real_time_event"] = {"status": "No significant event nearby."}

    with open(OUTPUT_JSON_REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=4, sort_keys=True)
if __name__ == "__main__":
    main()
